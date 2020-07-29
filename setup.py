import setuptools

setuptools.setup(
    name='pygor3',
    version='0.0.1',
    description='Python package to manipulate and run IGoR data files',
    license="GNU GPLv3",
    python_requires='>=3.5',
    install_requires = [
        "pandas",
        #"holoviz",
        "numpy",
        "xarray",
        "beautifulsoup4",
        "biopython"
    ],
    packages=setuptools.find_packages(),
    entry_points= {
        'console_scripts' : [
            'pygor3-observable=pygor3.scripts.observable:main',
            'pygor3-scriptTest=pygor3.scripts.scriptTest:main',
            'pygor3-scriptTest02=pygor3.scripts.scriptTest02:main',
            'pygor3-stas_from_bs=pygor3.scripts.stas_from_bs:main',
            'pygor3-load_database=pygor3.scripts.load_database:main',
            'pygor3-naive_align=pygor3.scripts.naive_align:main',
            'pygor3-naive_align_id=pygor3.scripts.naive_align_id:main',
            'pygor3-align_export=pygor3.scripts.align_export:main',
            'pygor3-bs_export=pygor3.scripts.bs_export:main',
            'igor-pgen_sequences=pygor3.scripts.pgen_sequences:main',
            'igor-infer_sequences=pygor3.scripts.infer_sequences:main',
            'igor-model_plot=pygor3.scripts.model_plot:main',
            #'igor-model_export=pygor3.scripts.model_export:main',
            'pygor3-model_export=pygor3.scripts.model_export:main',
            'pygor3-plot_marginals=pygor3.scripts.plot_marginals:main',
            'igor-model_create=pygor3.scripts.model_create:main',
            'igor-get_imgt_data=pygor3.scripts.get_imgt_data:main',
            'pygor3-download_imgt_gene_templates=pygor3.scripts.download_imgt_gene_templates:main',
            'pygor3-short_names_imgt_templates=pygor3.scripts.short_names_imgt_templates:main'
            #'igor-model_import=pygor3.model_import:main',
            #'igor-get_imgt_data=pygor3.get_imgt_data:main'
        ],
    }
)
