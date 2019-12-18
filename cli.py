import click
import logging

@click.group()
def cli():
    pass

@cli.command()
@click.argument("pdb-path", type=str)
@click.option("--src-regex", type=str, default="")
def show_pdb_source(pdb_path, src_regex):
    from srcsrv import SourceTool
    src_tool = SourceTool()
    for path in src_tool.scan_source_paths(pdb_path, src_regex):
        logging.info(path)

@cli.command()
@click.argument("pdb-path", type=str)
def show_pdb_index(pdb_path):
    from srcsrv import PDBStr
    pdb_str = PDBStr()
    logging.info(pdb_str.dump_index(pdb_path))

@cli.command()
@click.argument("pdb-path", type=str)
@click.argument("src-path", type=str)
@click.option("--src-regex", type=str, default="")
def make_svn_index(pdb_path, src_path, src_regex):
    from srcsrv import SourceTool
    src_tool = SourceTool()
    pdb_keys = src_tool.scan_source_paths(pdb_path, src_regex)

    from srcsrv import SVNIndex
    svn_index = SVNIndex()
    ini_path = os.path.splitext(pdb_path)[0] + '.srcsrv.ini'
    svn_index.make_ini(src_path, src_regex, pdb_keys, ini_path)

    from srcsrv import PDBStr
    pdb_str = PDBStr()
    logging.info(pdb_str.bind_index(pdb_path, ini_path))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()
