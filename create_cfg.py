from py2cfg import CFGBuilder

cfg = CFGBuilder().build_from_file("duyurular", "./duyurular.py")
cfg.build_visual("duyurular", "PDF")