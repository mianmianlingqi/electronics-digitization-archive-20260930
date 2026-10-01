"""Restore or verify all project ZIP packages with the SHA256 file manifest."""
import argparse, hashlib, json, os, pathlib, sys, zipfile

def long(p):
    p = str(pathlib.Path(p).absolute())
    return '\\\\?\\'+p if os.name=='nt' else p

def sha_file(path):
    h=hashlib.sha256()
    with open(long(path),'rb') as f:
        while b:=f.read(1024*1024): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--assets',required=True,type=pathlib.Path,help='Directory containing all downloaded release assets')
    ap.add_argument('--destination',type=pathlib.Path,help='Restore to this directory; an ExamBench subdirectory is created')
    ap.add_argument('--verify-only',action='store_true',help='Verify archives and every contained file without extracting')
    args=ap.parse_args()
    if not args.verify_only and args.destination is None: ap.error('--destination is required unless --verify-only is used')
    repo=pathlib.Path(__file__).resolve().parents[1]
    assets=json.loads((repo/'manifests/assets.json').read_text(encoding='utf-8'))
    rows=json.loads((repo/'manifests/files.json').read_text(encoding='utf-8'))
    grouped={}
    for row in rows: grouped.setdefault(row['asset'],[]).append(row)
    total=0
    for asset in assets:
        src=args.assets/asset['name']
        if not src.is_file(): raise RuntimeError('Missing asset: '+str(src))
        if src.stat().st_size!=asset['bytes'] or sha_file(src)!=asset['sha256']:
            raise RuntimeError('Asset SHA256 mismatch: '+asset['name'])
        if asset.get('role')=='original_input_archive':
            print('Verified original input archive:',asset['name'],flush=True)
            continue
        with zipfile.ZipFile(src) as z:
            expected=grouped[asset['name']]
            if len(z.infolist())!=len(expected): raise RuntimeError('Unexpected ZIP entry count: '+asset['name'])
            if set(z.namelist())!={r['path'] for r in expected}: raise RuntimeError('Unexpected ZIP path set: '+asset['name'])
            for row in expected:
                rel=pathlib.PurePosixPath(row['path'])
                if rel.is_absolute() or '..' in rel.parts or rel.parts[0]!='ExamBench':
                    raise RuntimeError('Unsafe archive path: '+row['path'])
                if z.getinfo(row['path']).file_size!=row['bytes']:
                    raise RuntimeError('ZIP size mismatch: '+row['path'])
                out=None
                if not args.verify_only:
                    dest=args.destination/pathlib.Path(*rel.parts)
                    if os.path.exists(long(dest)):
                        if sha_file(dest)!=row['sha256']:
                            raise RuntimeError('Refusing to replace different existing file: '+str(dest))
                    else:
                        os.makedirs(long(dest.parent),exist_ok=True)
                        out=open(long(dest),'wb')
                h=hashlib.sha256()
                try:
                    with z.open(row['path']) as f:
                        while b:=f.read(1024*1024):
                            h.update(b)
                            if out: out.write(b)
                finally:
                    if out: out.close()
                if h.hexdigest()!=row['sha256']: raise RuntimeError('File SHA256 mismatch: '+row['path'])
                if not args.verify_only:
                    os.utime(long(dest),ns=(row['mtime_ns'],row['mtime_ns']))
                total+=1
        print(f"Verified {asset['name']}: {len(expected)} files ({total}/{len(rows)})",flush=True)
    print(json.dumps({'all_files_verified':True,'files':total,'assets':len(assets),'restore':not args.verify_only}),flush=True)

if __name__=='__main__': main()
