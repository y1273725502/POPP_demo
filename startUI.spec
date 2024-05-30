# -*- mode: python ; coding: gbk -*-


a = Analysis(
    ['startUI.py','chloroplast_tax.py', 'ch_find_pair_species.py', 'ch_next.py', 'ch_speciesManage.py', 'ch_viewAllGenome.py', 'clustal.py', 'completeGeneToTxt.py', 'conservedSequence.py', 'demo.py', 'downloadCompleteGenome.py', 'download_file.py', 'Fasttree.py', 'FastTreeUi.py', 'fas_to_nex.py', 'filter_chloroplast.py', 'filter_mitochondrial.py', 'findAllGene.py', 'finderRes.py', 'firstUI.py', 'geneForEachSpec.py', 'genes.py', 'geneSelection.py', 'geneToFolder.py', 'get_chloroplast_nuccore_result.py', 'get_mitochondria_nuccore_result.py', 'iqTree.py', 'iqTreeUI.py', 'mafftWay.py', 'mitochondrial_tax.py', 'mi_find_pair_species.py', 'mi_next.py', 'mi_speciesManage.py', 'mi_viewAllGenome.py', 'model_finder.py', 'mrbayes.py', 'MrBayesUI.py', 'Muscle.py', 'next.py', 'nj_tree.py', 'nj_treeUI.py', 'PAML.py', 'PAML_Res.py', 'PAML_UI.py', 'seeAlignRes.py', 'seeGenomeUI.py', 'specAllGene.py', 'split_to_fasta.py', 'split_to_txt.py', 'split_to_txt1.py', 'tax_info_chloroplast.py', 'tax_info_mitochondrial.py', 'toTreeUI.py', 'tree.py', 'treeUI.py', 'tre_to_newick.py', 'trimal.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='startUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
