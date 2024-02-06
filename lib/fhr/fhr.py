import yaml
import json
import microdata
import re
from jsonschema import validate

schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://raw.githubusercontent.com/FAIR-bioHeaders/FHR-Specification/main/fhr.json",
  "title": "FHR",
  "description": "FAIR Header Reference genome Schema for Genome Assemblies",
  "type": "object",
  "properties": {
    "schema":{
      "type": "string",
      "description": "centralized schema file"
    },
    "schemaVersion":{
      "type": "number",
      "description": "Version of FHR"
    },
    "genome":{
      "type": "string",
      "description": "Name of the Genome"
    },
    "genomeSynonym": {
      "type": "array",
      "description": "Other common names of the genome",
      "items": {
        "type":"string"
      }
    },
    "taxon":{
      "type": "object",
      "description": "Species name and URL of the species information at identifiers.org",
      "properties": {
        "name": {
          "type": "string"
        },
        "uri": {
          "type": "string",
          "format": "uri",
          "pattern": "https://identifiers.org/taxonomy:[0-9]+"
        }
      }
    },
    "version":{
      "type": "string",
      "description": "Version number of Genome eg. 1.2.0"
    },
    "metadataAuthor":{
      "type": "array",
      "items": {
        "type": "object",
        "description": "Author of the FHR Instance (Person or Org)",
        "properties": {
          "name": {
            "type": "string"
          },
          "uri": { "$ref": "#/definitions/orcidUri" }
        }
      }
    },
    "assemblyAuthor":{
      "type": "array",
        "items": {
        "type": "object",
        "description": "Assembler of the Genome (Person or Org)",
        "properties": {
          "name": {
            "type": "string"
          },
          "uri": { "$ref": "#/definitions/orcidUri" }
        }
      }
    },
    "dateCreated":{
      "type": "string",
      "format": "date",
      "description": "Date the genome assembly was created"
    },
    "voucherSpecimen":{
      "type": "string",
      "description": "Description of the physical sample"
    },
    "accessionID":{
      "type": "object",
      "description": "accessionID genome assembly was created",
      "properties": {
        "name": {
          "type": "string"
        },
        "url": {
          "type": "string",
          "format": "uri"
        }
      }
    },
    "instrument": {
      "type": "array",
      "description": "Physical tools and instruments used in the creation of the genome assembly",
      "items": {
        "type": "string"
      }
    },
    "scholarlyArticle": {
      "type": "string",
      "pattern": "^10.",
      "description": "Scholarly article genome was published e.g. 10.5281/zenodo.6762550 "
    },
    "documentation": {
      "type": "string",
      "description": "Documentation about the genome"
    },
    "identifier": {
      "type": "array",
      "description": "Identifies of the genome",
      "items": {
        "type": "string",
        "pattern": "[a-z0-9]*:.*"
        }
    },
    "relatedLink": {
      "type": "array",
      "description": "Related URLS to the genome",
      "items": {
        "type": "string",
        "format": "uri"
      }
    },
    "funding": {
      "type": "string",
      "description": "Grant Line Item"
    },
    "license": {
      "type": "string",
      "description": "license for the use of the Genome"
    },
    "masking": {
      "type": "string",
      "pattern": "(not-masked|hard-masked|soft-masked|repeat-masked)",
    "description": "masking applied to the genome assembly"
    },
    "vitalStats": {
      "type": "object",
      "description": "general statistics about the genome assembly",
      "properties": {
        "L50": {
            "type": "integer",
            "description": "L50 of the genome assembly"
        },
        "N50": {
            "type": "integer",
             "description": "N50 of the genome assembly"
        },
        "L90": {
            "type": "integer" ,
            "description": "L90 of the genome assembly"
        },
        "totalBasePairs": {
            "type": "integer" ,
            "description": "total base pairs of the genome assembly"
        },
        "numberContigs": {
            "type": "integer" ,
            "description": "number of contigs of the genome assembly"
        },
        "numberScaffolds": {
            "type": "integer" ,
            "description": "number of scaffolds of the genome assembly"
        },
        "readTechnology": {
            "type": "string",
            "description": "read technology of the genome assembly (short, long, hifi, etc...)"
        }
      }
    },
    "checksum": { "$ref": "#/definitions/sha2" }
  },
  "required": [
    "schema",
    "schemaVersion",
    "genome",
    "taxon",
    "version",
    "metadataAuthor",
    "assemblyAuthor",
    "dateCreated",
    "masking",
    "checksum"
  ],
  "definitions": {
    "orcidUri": { "format": "uri",
                  "pattern": "^https://orcid.org/[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9X]" },
    "sha2": {
      "type": "string",
      "minLength": 44,
      "maxLength": 44,
      "pattern": "^[A-Za-z0-9/+=]+$",
      "description": "sha2-512/256 checksum value for hashing"
    }
  },
  "additionalProperties": false
}


class fhr:

    def __init__(self, schema=None, version=None, schemaVersion=None, genome=None, assemblySoftware=None, voucherSpecimen=None, dateCreated=None, scholarlyArticle=None, documentation=None, reuseConditions=None, masking=None, checksum=None):
        self.schema = schema
        self.version = version
        self.schemaVersion = schemaVersion
        self.genome = genome
        self.genomeSynonym = []
        self.metadataAuthor = []
        self.assemblyAuthor = []
        self.accessionID = dict()
        self.taxon = dict()
        self.assemblySoftware = assemblySoftware
        self.voucherSpecimen = voucherSpecimen
        self.dateCreated = dateCreated
        self.instrument = []
        self.scholarlyArticle = scholarlyArticle
        self.documentation = documentation
        self.identifier = []
        self.relatedLink = []
        self.funding = []
        self.masking = masking
        self.vitalStats = []
        self.reuseConditions = reuseConditions
        self.checksum = checksum

    #def __repr__(self): # noqa
    #    return "%s(schemaVersion=%r, version=%r, genome=%r)" % ( # noqa
    #       self.schemaVersion, self.version, self.genome) # noqa

    #def __str__(self): # noqa
    #    return f'("{self.schemaVersion},{self.version},{self.genome}")' # noqa

    def input_yaml(self, stream: str):
        data = yaml.safe_load(stream)
        self.schema = data['schema']
        self.version = data['version']
        self.schemaVersion = data['schemaVersion']
        self.genome = data['genome']
        self.genomeSynonym = data['genomeSynonym']
        self.metadataAuthor = data["metadataAuthor"]
        self.assemblyAuthor = data["assemblyAuthor"]
        self.accessionID["name"] = data["voucherID"]["name"]
        self.accessionID["url"] = data["accessionID"]["url"]
        self.taxon["name"] = data["taxon"]["name"]
        self.taxon["uri"] = data["taxon"]["uri"]
        self.assemblySoftware = data["assemblySoftware"]
        self.voucherSpecimen = data["voucherSpecimen"]
        self.dateCreated = data["dateCreated"]
        self.instrument = data["instrument"]
        self.scholarlyArticle = data["scholarlyArticle"]
        self.documentation = data["documentation"]
        self.identifier = data["identifier"]
        self.relatedLink = data["relatedLink"]
        self.funding = data["funding"]
        self.masking = data["masking"]
        self.vitalStats["N50"]
        self.vitalStats["L50"]
        self.vitalStats["L90"]
        self.vitalStats["totalBasePairs"]
        self.vitalStats["numberContigs"]
        self.vitalStats["numberScaffolds"]
        self.vitalStats["readTechnology"]
        self.reuseConditions = data["reuseConditions"]
        self.checksum = data["checksum"]

    def output_yaml(self):
        return yaml.dump(self.__dict__)

    def input_fasta(self, stream: str):
        formulated = ""
        data = re.findall(';~.*', stream)
        for value in stream:
            formulated = formulated + "\n" + re.sub(';~', '', value)
        self.yaml(formulated)

    def output_fasta(self):
        array = ';~- '
        name = '\n;~- name:'
        uri = '\n;~  uri:'
        end_span = ''

        data = (
            f';~schema: {self.schema}\n'
            f';~schemaVersion: {self.schemaVersion}\n'
            f';~genome: {self.genome}\n'
            f';~genomeSynonym:\n'
            f'{array + array.join(x + end_span for x in self.genomeSynonym)}'
            f';~version: {self.version}\n'
            f';~metadataAuthor:'
            f'{name + name.join(name + x["name"] + uri + x["uri"] for x in self.metadataAuthor)}'
            f'\n;~assemblyAuthor:'
            f'{name + name.join(name + x["name"] + uri + x["uri"] for x in self.assemblyAuthor)}'
            f';~accessionID:\n'
            f';~  name:{self.accessionID["name"]}\n'
            f';~  url:{self.accessionID["url"]}\n'
            f';~taxon:\n'
            f';~  name:{self.taxon["name"]}\n'
            f';~  uri:{self.taxon["uri"]}\n'
            f';~assemblySoftware: {self.assemblySoftware}\n'
            f';~voucherSpecimen: {self.voucherSpecimen}\n'
            f';~dateCreated: {self.dateCreated}\n'
            f';~instrument:\n'
            f'{array + array.join(x + end_span for x in self.instrument)}'
            f';~scholarlyArticle: {self.scholarlyArticle}\n'
            f';~documentation: {self.documentation}\n'
            f';~identifier:\n'
            f'{array + array.join(x + end_span for x in self.identifier)}'
            f';~relatedLink:\n'
            f'{array + array.join(x + end_span for x in self.relatedLink)}'
            f';~funding:\n'
            f'{array + array.join(x + end_span for x in self.funding)}'
            f';~masking {self.masking}\n'
            f';~vitalStats:\n'
            f';~-N50: {self.vitalStats["N50"]}\n'
            f';~-L50: {self.vitalStats["L50"]}\n'
            f';~-L90: {self.vitalStats["L90"]}\n'
            f';~-totalBasePairs: {self.vitalStats["totalBasePairs"]}\n'
            f';~-numberContigs: {self.vitalStats["numberContigs"]}\n'
            f';~-numberScaffolds: {self.vitalStats["numberScaffolds"]}\n'
            f';~-readTechnology: {self.vitalStats["readTechnology"]}\n'
            f';~reuseConditions: {self.reuseConditions}\n'
            f';~checksum: {self.checksum}\n'
        )

        return data

    def input_microdata(self, stream: str):
        data = microdata.get_items(stream)
        data = data[0]
        self.schema = data.schema
        self.version = data.version
        self.schemaVersion = data.schemaVersion
        self.genome = data.genome
        self.genomeSynonym = data.get_all('genomeSynonym')
        self.metadataAuthor = data.get_all('metadataAuthor')
        self.assemblyAuthor = data.get_all('assemblyAuthor')
        self.accessionID["name"] = data.accessionID
        self.accessionID["url"] = data.accessionID.url
        self.taxon["name"] = data.taxon.name
        self.taxon["uri"] = data.taxon.uri
        self.assemblySoftware = data.assemblySoftware
        self.voucherSpecimen = data.voucherSpecimen
        self.dateCreated = data.dateCreated
        self.instrument = data.get_all('instrument')
        self.scholarlyArticle = data.scholarlyArticle
        self.documentation = data.documentation
        self.identifier = data.get_all('identifier')
        self.relatedLink = data.get_all('relatedLink')
        self.funding = data.get_all('funding')
        self.masking = data.masking
        self.vitalStats = data.get_all('vitalStats')
        self.reuseConditions = data.reuseConditions
        self.checksum = data.checksum

    def output_microdata(self):
        instrument = '<span itemprop="instrument">'
        identifier = '<span itemprop="identifier">'
        relatedLink = '<span itemprop="relatedLink">'
        funding = '<span itemprop="funding">'
        metadataAuthor = '<span itemprop="metadataAuthor">'
        assemblyAuthor = '<span itemprop="assemblyAuthor">'
        genomeSynonym = '<span itemprop="genomeSynonym">'
        name = '<span itemprop="name">'
        uri = '<span itemprop="uri">'
        end_span = "</span>"

        data = (
            f'<div itemscope itemtype="https://raw.githubusercontent.com/FAIR-bioHeaders/FHR-Specification/main/fhr.json" version="{self.schemaVersion}">'
            f'<span itemprop="schema">{self.schema}</span>'
            f'<span itemprop="schemaVersion">{self.schemaVersion}</span>'
            f'<span itemprop="version">{self.version}</span>'
            f'<span itemprop="genome">{self.genome}</span>'
            f'{genomeSynonym + genomeSynonym.join(x + end_span for x in self.genomeSynonym)}'
            f'{metadataAuthor + metadataAuthor.join(name + x["name"] + end_span + uri + x["uri"] + end_span for x in self.metadataAuthor)}'
            f'</span>'
            f'{assemblyAuthor + assemblyAuthor.join(name + x["name"] + end_span + uri + x["uri"] + end_span for x in self.assemblyAuthor)}'
            f'</span>'
            f'<span itemprop="accessionID">'
            f'  <span itemprop="name">{self.accessionID["name"]}</span>'
            f'  <span itemprop="url">{self.accessionID["url"]}"</span>'
            f'</span>'
            f'<span itemprop="taxon">'
            f'  <span itemprop="name">self.taxon["name"]</span>'
            f'  <span itemprop="uri">self.taxon["uri"]</span>'
            f'</span>'
            f'<span itemprop="assemblySoftware">{self.assemblySoftware}</span>'
            f'<span itemprop="voucherSpecimen">{self.voucherSpecimen}</span>'
            f'<span itemprop="dateCreated">{self.dateCreated}</span>'
            f'{instrument + instrument.join(x + end_span for x in self.instrument)}'
            f'<span itemprop="scholarlyArticle">{self.scholarlyArticle}</span>'
            f'<span itemprop="documentation">{self.documentation}</span>'
            f'{identifier + identifier.join(x + end_span for x in self.identifier)}'
            f'{relatedLink + relatedLink.join(x + end_span for x in self.relatedLink)}'
            f'{funding + funding.join(x + end_span for x in self.funding)}'
            f'<span itemprop="masking">{self.masking}<\span>'
            f'<span itemprop="vitalStats">'
            f'  <span itemprop="N50">{self.vitalStats["N50"]}<\span>'
            f'  <span itemprop="L50">self.vitalStats["L50"]}<\span>'
            f'  <span itemprop="L90">{self.vitalStats["L90"]}<\span>'
            f'  <span itemprop="totalBasePairs">{self.vitalStats["totalBasePairs"]}<\span>'
            f'  <span itemprop="numberContigs">{self.vitalStats["numberContigs"]}<\span>'
            f'  <span itemprop="numberScaffolds">{self.vitalStats["numberScaffolds"]}<\span>'
            f'  <span itemprop="readTechnology">{self.vitalStats["readTechnology"]}<\span>'
            f'</span>'
            f'<span itemprop="reuseConditions">{self.reuseConditions}</span>'
            f'<span itemprop="checksum">{self.checksum}</span>'
            f'</div>'
        )

        return data

    def input_json(self, stream: str):
        data = json.loads(stream)
        data = yaml.safe_load(stream)
        self.schema = data['schema']
        self.version = data['version']
        self.schemaVersion = data['schemaVersion']
        self.genome = data['genome']
        self.genomeSynonym = data['genomeSynonym']
        self.metadataAuthor = data["metadataAuthor"]
        self.assemblyAuthor = data["assemblyAuthor"]
        self.accessionID["name"] = data["accessionID"]["name"]
        self.accessionID["url"] = data["accessionID"]["url"]
        self.taxon["name"] = data["taxon"]["name"]
        self.taxon["uri"] = data["taxon"]["uri"]
        self.assemblySoftware = data["assemblySoftware"]
        self.voucherSpecimen = data["voucherSpecimen"]
        self.dateCreated = data["dateCreated"]
        self.instrument = data["instrument"]
        self.scholarlyArticle = data["scholarlyArticle"]
        self.documentation = data["documentation"]
        self.identifier = data["identifier"]
        self.relatedLink = data["relatedLink"]
        self.funding = data["funding"]
        self.masking = data["masking"]
        self.vitalStats = data["vitalStats"]
        self.reuseConditions = data["reuseConditions"]
        self.checksum = data["checksum"]

    def output_json(self):
        return json.dumps(self.__dict__)

    def input_gfa(self, stream: str):
        formulated = ""
        data = re.findall('#~.*', stream)
        for value in stream:
            formulated = formulated + "\n" + re.sub('#~', '', value)
        self.yaml(formulated)

    def output_gfa(self):
        array = '#~- '
        name = '\n;~- name:'
        uri = '\n;~  uri:'
        end_span = ''

        data = (
            f'#~schema: {self.schema}\n'
            f'#~schemaVersion: {self.schemaVersion}\n'
            f'#~genome: {self.genome}\n'
            f'#~genomeSynonym:\n'
            f'{array + array.join(x + end_span for x in self.genomeSynonym)}'
            f'#~version: {self.version}\n'
            f'#~metadataAuthor:'
            f'{name + name.join(name + x["name"] + uri + x["uri"] for x in self.metadataAuthor)}'
            f'\n;~assemblyAuthor:'
            f'{name + name.join(name + x["name"] + uri + x["uri"] for x in self.assemblyAuthor)}'
            f'#~accessionID:\n'
            f'#~  name:{self.accessionID["name"]}\n'
            f'#~  url:{self.accessionID["url"]}\n'
            f'#~taxon:\n'
            f'#~  name:{self.taxon["name"]}\n'
            f'#~  uri:{self.taxon["uri"]}\n'
            f'#~assemblySoftware: {self.assemblySoftware}\n'
            f'#~voucherSpecimen: {self.voucherSpecimen}\n'
            f'#~dateCreated: {self.dateCreated}\n'
            f'#~instrument:\n'
            f'{array + array.join(x + end_span for x in self.instrument)}'
            f'#~scholarlyArticle: {self.scholarlyArticle}\n'
            f'#~documentation: {self.documentation}\n'
            f'#~identifier:\n'
            f'{array + array.join(x + end_span for x in self.identifier)}'
            f'#~relatedLink:\n'
            f'{array + array.join(x + end_span for x in self.relatedLink)}'
            f'#~funding:\n'
            f'{array + array.join(x + end_span for x in self.funding)}'
            f'#~masking {self.masking}\n'
            f'#~vitalStats:\n'
            f'#~-N50: {self.vitalStats["N50"]}\n'
            f'#~-L50: {self.vitalStats["L50"]}\n'
            f'#~-L90: {self.vitalStats["L90"]}\n'
            f'#~-totalBasePairs: {self.vitalStats["totalBasePairs"]}\n'
            f'#~-numberContigs: {self.vitalStats["numberContigs"]}\n'
            f'#~-numberScaffolds: {self.vitalStats["numberScaffolds"]}\n'
            f'#~-readTechnology: {self.vitalStats["readTechnology"]}\n'
            f'#~reuseConditions: {self.reuseConditions}\n'
            f'#~checksum: {self.checksum}\n'
        )

        return data

    def fhr_validate(self):
        fhr_instance = json.dumps(self.__dict__)
        validate(instance=fhr_instance, schema=schema)
