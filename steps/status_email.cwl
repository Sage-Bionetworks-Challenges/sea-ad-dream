#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

label: Email scores
doc: >
  Send an email of the evaluation scores back to the submitter and, if on a
  submission team, their teammates.

requirements:
- class: InlineJavascriptRequirement
- class: InitialWorkDirRequirement
  listing:
  - entryname: score_email.py
    entry: |
        #!/usr/bin/env python
        import argparse
        import json
        import os

        import synapseclient

        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--submissionid", required=True, help="Submission ID")
        parser.add_argument("-c", "--synapse_config", required=True, help="credentials file")
        parser.add_argument("-r", "--results", required=True, help="Resulting scores")

        args = parser.parse_args()
        syn = synapseclient.Synapse(configPath=args.synapse_config)
        syn.login()

        sub = syn.getSubmission(args.submissionid)
        participantid = sub.get("teamId")
        if participantid is not None:
            name = syn.getTeam(participantid)["name"]
        else:
            participantid = sub.userId
            name = syn.getUserProfile(participantid)["userName"]
        evaluation = syn.getEvaluation(sub.evaluationId)
        with open(args.results) as json_data:
            annots = json.load(json_data)
        if annots.get("submission_status") is None:
            raise Exception("score.cwl must return submission_status as a json key")
        status = annots["submission_status"]

        subject = f"Submission to '{evaluation.name}' - Evaluation Status"
        message = f"Hello {name}, \n\n"
        if status == "SCORED":
            message += f"Your submission (id: {sub.id}) has been scored! Results will be announced at a later time."
        else:
            message += f"Error encountered during scoring; your submission (id: {sub.id}) was not evaluated."
        message += "\n\nSincerely,\nChallenge Administrator"
        syn.sendMessage(
            userIds=[participantid], messageSubject=subject, messageBody="".join(message)
        )

inputs:
- id: submissionid
  type: int
- id: synapse_config
  type: File
- id: results
  type: File

outputs: []

baseCommand: python3
arguments:
- valueFrom: score_email.py
- prefix: -s
  valueFrom: $(inputs.submissionid)
- prefix: -c
  valueFrom: $(inputs.synapse_config.path)
- prefix: -r
  valueFrom: $(inputs.results)

hints:
  DockerRequirement:
    dockerPull: sagebionetworks/synapsepythonclient:v3.1.1