# FHT-File-Converter
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6762547.svg)](https://doi.org/10.5281/zenodo.6762547)

This is the fht file converter, it can convert fht inbetween json, fasta, microdata, and fasta header. If you would like a detailed specification of fht, see [FHT-Specification](https://github.com/FAIR-bioHeaders/FHT-Specification)

## Installation

You can intall the FHT file converter via pypi:

```bash 
pip install fhT
```

You can also install the FHT file converter and its dependencies using Poetry (by first downloading the repo or release):

```bash
poetry install
```

## Usage


### Commnand line Usage

Using FHT on the command line:

```bash
fht-convert <input>.<yaml|json|fasta|html> <output>.<yaml|json|fasta|html>
```

Detailed Usage:

```
usage: fht-convert [-h] [--version] <file> <file>

Convert from one FHT supported file type to another

positional arguments:
  <file>      input followed by output

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit

positional <file> input and output files
    input files can be one of:
        <input>.yml
        <input>.fasta  - fasta contining a fht header
        <input>.html   - html containing microdata

    output files can be one of:
        <output>.yml
        <output>.fasta - fasta output type will be made as a fasta header without sequences
        <output>.html  - microdata output type will be made into generic html output
```

## Validating an FHT file on command line


```bash
fht-validate <input>.<yaml|json|fasta|html>
```

Detailed Usage:

```
usage: fht-validate [-h] [--version] <file>

Validate a fht containing file

 positional <file> input and output files
                        input files can be one of:
                            <input>.yml
                            <input>.fasta  - fasta contining a fht header
                            <input>.html   - html containing microdata
```


As such validating a yaml file named "important\_transcriptome.fht.yml" would be:

`fht-validate important_transcriptome.fht.yml`


## Other FHR Tools

FHT has several other command line tools:

* `fht_fasta_combine` - combine a fht header in any serialization with an existing fasta file
* `fht_fasta_strip` - remove a fht header out of a fasta file
* `fht_fasta_validate` - check an fht containing fasta against its checksum 
* `fht_gfa_combine` - combine a fht header in any serilaization with an existing gfa file
* `fht_gfa_strip` - remove an fht header our of a gfa file
* `fht_gfa_validate` - check an fht containing gfa against its checksum

## Using FHT in Python

To use FHT libabry in Python

```python
>>> from fht import fht
>>> file = open("example.yaml")
>>> data = fht()
>>> data.input_yaml(file.read())
>>> data.output_fasta()
";~schema: https://raw.githubusercontent.com/FFRGS/FFRGS-Specification/main/fht.json\n;~schemaVersion: 1\n;~transcriptome: Bombas huntii\n;~version: 0.0.1\n;~author:;~  name:Adam Wright\n;~  url:https://wormbase.org/resource/person/WBPerson30813\n;~assembler:;~  name:David Molik\n;~  url:https:/david.molik.co/person\n;~place:;~  name:PBARC\n;~  url:https://www.ars.usda.gov/pacific-west-area/hilo-hi/daniel-k-inouye-us-pacific-basin-agricultural-research-center/\n;~taxa: Bombas huntii\n;~assemblySoftware: HiFiASM\n;~physicalSample: Located in Freezer 33, Drawer 137\n;~dateCreated: 2022-03-21\n;~instrument: ['Sequel IIe', 'Nanopore']\n;~scholarlyArticle: https://doi.org/10.1371/journal.pntd.0008755\n;~documentation: Built assembly from... \n;~identifier: ['gkx10242566416842']\n;~relatedLink: ['https/david.molik.co/transciptome']\n;~funding: some\n;~reuseConditions: public domain\n"
```

## Checksums

The FHT stores checksums, allowing the FASTA header of the reference transcriptome to contain the checksum for the FASTA file without the header.

To utilize the checksum, strip the FASTA header:

```bash
cat example.fasta | grep -E -v '^;~\s?checksum'  > example.check.fasta
```

To strip the checksum:


```bash
cat example.fasta | grep -E ';~\s?checksum' | sed 's/^;~checksum://g' | sed '/\'//g'
```

## Docker Support

You can also run the FHT file converter in a Docker container. To build the Docker image:

```bash
docker build -t fht-file-converter .
```

And then run the Docker container:

```bash
docker run -it --rm fht-file-converter
```


## Running Code Quality Checks

Ensuring code quality is crucial for maintaining a healthy and sustainable codebase. The following tools help enforce coding standards and best practices:

### isort

`isort` is a tool that sorts Python imports alphabetically within each section and separated by a blank line. It ensures consistent import styles across your project.

To run isort, use the following command:

```bash
poetry run isort .
```

### ruff
ruff is a lightweight linter for Python that aims to detect common programming errors, stylistic issues, and code smells. It provides quick feedback on potential issues in your code.

To run ruff, use the following command:

```bash
poetry run ruff .
```

### black

`black` is an uncompromising Python code formatter. It reformats entire files in place to ensure a consistent and readable code style. It's opinionated and strives for the smallest diffs possible.

To run black, use the following command:

```bash
poetry run black .
```

Running these code quality checks regularly helps maintain a clean and consistent codebase, making it easier to collaborate with others and ensuring code readability and maintainability. These checks are required to pass in order to pull changes into the main branch. 


### pytest

Make sure you install depedencies first and then run the tests with poetry
```bash
poetry run install
poetry run pytest
```

## Related FHR citations

These DOI records identify FHR resources; they must not be represented as
FHT-specific release DOIs. Use resource-specific metadata for FHT citations.


Chicago bibliography entries are used below. Cite the published paper for a
general description of FHR; cite the specification or converter when using that
resource directly. The software and specification links are concept DOIs; for a
specific release, use the corresponding version DOI from Zenodo. Authors and
years follow the records resolved by the concept DOIs at the v0.3 documentation
update, and can change as later records are published.

### Published paper

Wright, Adam, Mark D. Wilkinson, Christopher Mungall, Scott Cain, Stephen Richards, Paul Sternberg, Ellen Provin, Jonathan L. Jacobs, Scott Geib, Daniela Raciti, Karen Yook, Lincoln Stein, and David C. Molik. “FAIR Header Reference Genome: A TRUSTworthy Standard.” *Briefings in Bioinformatics* 25, no. 3 (2024): bbae122. https://doi.org/10.1093/bib/bbae122.

### Specification

Molik, David. *FHR Specification*. Data set. 2022. https://doi.org/10.5281/zenodo.6762549.

### Converter

Molik, David, and Adam Wright. *FHR File Converter*. Computer software. 2024. https://doi.org/10.5281/zenodo.6762547.

Machine-readable entries are maintained in
[FHR-Citation](https://github.com/FAIR-bioHeaders/FHR-Citation/blob/main/citation.bib).

## Licensing

[![License: MPL-2.0](https://img.shields.io/badge/License-MPL--2.0-blue.svg)](LICENSE)

New project contributions from March 2025 onward use [MPL-2.0](LICENSE). David Molik left USDA in February 2025. Historical USDA public-domain material remains public domain within the United States; its original notice is preserved in LICENSE. Previously granted permissions and third-party terms remain intact. The project includes both historical material and subsequent MPL-2.0 contributions; file notices and history identify provenance.
