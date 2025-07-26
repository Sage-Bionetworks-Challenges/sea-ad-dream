#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
label: Sample CWL sub-script

inputs:
- id: message
  type: string
  default: "Hello, World!"

outputs: []

baseCommand: echo
arguments:
  - valueFrom: $(inputs.message)

s:author:
- class: s:Person
  s:identifier: https://orcid.org/0000-0002-5622-7998
  s:email: verena.chung@sagebase.org
  s:name: Verena Chung

s:codeRepository: https://github.com/Sage-Bionetworks-Challenges/sea-ad-dream
s:license: https://spdx.org/licenses/Apache-2.0

$namespaces:
  s: https://schema.org/
