#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
label: BraTS 2025 - Docker submission workflow

requirements:
  - class: StepInputExpressionRequirement

inputs:
  adminUploadSynId:
    label: Synapse Folder ID accessible by an admin
    type: string
  submissionId:
    label: Submission ID
    type: int
  submitterUploadSynId:
    label: Synapse Folder ID accessible by the submitter
    type: string
  synapseConfig:
    label: filepath to .synapseConfig file
    type: File
  workflowSynapseId:
    label: Synapse File ID that links to the workflow
    type: string
  organizers:
    label: User or team ID for challenge organizers
    type: string
    default: "3542567"

outputs: []

steps:
  01_hello_world
    doc: "This is a placeholder step to demonstrate workflow structure."
    run: steps/hello_world.cwl
    in:
      - id: message
        default: "Hello, World!"
    out: []

s:author:
- class: s:Person
  s:identifier: https://orcid.org/0000-0002-5622-7998
  s:email: verena.chung@sagebase.org
  s:name: Verena Chung

s:codeRepository: https://github.com/Sage-Bionetworks-Challenges/sea-ad-dream
s:license: https://spdx.org/licenses/Apache-2.0

$namespaces:
  s: https://schema.org/