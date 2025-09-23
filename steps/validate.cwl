#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
label: Validate segmentation submission

requirements:
- class: InlineJavascriptRequirement

inputs:
- id: input_file
  type: File
- id: groundtruth
  type: File
- id: previous_annotation_finished
  type: boolean?

outputs:
- id: results
  type: File
  outputBinding:
    glob: results.json
- id: status
  type: string
  outputBinding:
    glob: results.json
    outputEval: $(JSON.parse(self[0].contents)['submission_status'])
    loadContents: true
- id: invalid_reasons
  type: string
  outputBinding:
    glob: results.json
    outputEval: $(JSON.parse(self[0].contents)['submission_errors'])
    loadContents: true

baseCommand: validate.py
arguments:
- prefix: -p
  valueFrom: $(inputs.input_file)
- prefix: -g
  valueFrom: $(inputs.groundtruth.path)
- prefix: -o
  valueFrom: results.json

hints:
  DockerRequirement:
    dockerPull: ghcr.io/sage-bionetworks-challenges/sea-ad-dream:v0.0.3

s:author:
- class: s:Person
  s:identifier: https://orcid.org/0000-0002-5622-7998
  s:email: verena.chung@sagebase.org
  s:name: Verena Chung

s:codeRepository: https://github.com/Sage-Bionetworks-Challenges/sea-ad-dream

$namespaces:
  s: https://schema.org/