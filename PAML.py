from Bio.Phylo.PAML import codeml


def run_paml(seqfile, treefile, out_file, seqtype=1, noisy=0, RateAncestor=0, model=0, NSsites=[0],
             CodonFreq=2, cleandata=1, fix_alpha=1, kappa=4.54006):
    """
    Run PAML codeml analysis.

    Parameters:
    - seqfile: Path to the sequence file.
    - treefile: Path to the tree file.
    - out_file: Path for the output file.
    - seqtype: Type of sequences (1: codons; 2: AAs; 3: Codons <-> AAs).
    - verbose: Verbose level (0: minimal output; 1: detailed output).
    - noisy: Control over the screen output (0-9).
    - RateAncestor: Ancestral reconstruction (0: none; 1: marginal; 2: joint).
    - model: Models of substitution (0-9).
    - NSsites: Models of site-specific rates (0: one rate; 1: neutral; 2: selection, etc.).
    - CodonFreq: Codon frequency model (0-3).
    - cleandata: Remove ambiguous data from alignment (0: no; 1: yes).
    - fix_alpha: Fix alpha to a value (1: yes; 0: no).
    - kappa: Transition/transversion rate ratio.
    """
    with open(seqfile, 'r') as f:
        content = f.read()
        content = content.replace("tag", "---")
        content = content.replace("taa", "---")
        content = content.replace("tga", "---")
        print(content)

    with open(seqfile, 'w') as f:
        f.write(content)

    cml = codeml.Codeml()
    cml.alignment = seqfile
    cml.tree = treefile
    cml.out_file = out_file
    cml.set_options(seqtype=seqtype, verbose=True, noisy=noisy, RateAncestor=RateAncestor, model=model,
                    NSsites=NSsites, CodonFreq=CodonFreq, cleandata=cleandata, fix_alpha=fix_alpha, kappa=kappa)

    cml.run(verbose=True)
    print(f"Analysis completed. Results are in {out_file}")


# Example usage
#run_paml(r"C:\Users\12737\Documents\Capstone_project\2024-03-27-16-29-39\temp.fasta",r"C:\Users\12737\Documents\Capstone_project\2024-03-27-16-29-39\temp.fasta.treefile", "2024-03-27-16-29-39/output_file")
