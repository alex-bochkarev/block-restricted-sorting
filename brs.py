from itertools import combinations
from argparse import ArgumentParser

def inversions(A, verbose=False):
    """Calculates the number of inversions in `A`.

    Prints the inversions (one per line) if `verbose` is set to `True`.
    """
    invs = 0
    for i in range(len(A)-1):
        for j in range(i, len(A)):
            if A[i] > A[j]:
                if verbose: print(f"{A[i], A[j]}")
                invs += 1

    return invs


def inv_score(A,B, verbose = False):
    """Computes the 'inversion score'.

    Negative score implies "A < B." Prints the respective inversions
    in both cases (in `(A,B)` and `(B,A)`) if `verbose` is set to `True`.
    """
    if verbose:
        print(f"{A} -> {B}:")

    iAB = inversions(A+B, verbose)

    if verbose:
        print(f"{iAB} in total.\n***")
        print(f"{B} -> {A}:")

    iBA = inversions(B+A, verbose)

    if verbose: print(f"{iBA} in total.")
    return iAB - iBA


def load_blocks(filename):
    """Loads blocks from the file named `filename`.

    Returns:
        Dict of blocks, a string `b<num>` (key) -> list of numbers in the block (value).
    """
    blocks = {}

    with open(filename, "r") as bfile:
        nblock = 1
        for line in bfile.readlines():
            blocks[f"b{nblock}"] = [int(x) for x in line.split(",")]
            nblock += 1

    return blocks


def make_dia(blocks, outfile="./blocks.dot"):
    """Creates a `dot` file depicting `blocks` and saves it to file named `outfile`."""
    with open(outfile, "w") as outf:
        outf.write("digraph blocks {\n")
        for n in blocks.keys():
            outf.write(f"    {n} [label=\"{n}: {blocks[n]}\"];\n")

        for (n1,n2) in combinations(blocks, 2):
                if n1 != n2:
                    if inv_score(blocks[n1], blocks[n2]) <= 0:
                        outf.write(f"    {n1} -> {n2};\n")
                    if inv_score(blocks[n1], blocks[n2]) >= 0:
                        outf.write(f"    {n2} -> {n1};\n")
        outf.write("}")


def main():
    parser = ArgumentParser()
    parser.add_argument("infile", help="*.blocks file name")
    parser.add_argument("outfile", help="*.dot file name")
    args = parser.parse_args()

    blocks = load_blocks(args.infile)
    make_dia(blocks, args.outfile)


if __name__ == '__main__':
    main()
