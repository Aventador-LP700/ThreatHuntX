# Your first 10 minutes

Start the [Community Lab](GETTING_STARTED.md) and open <http://127.0.0.1:8080/>. Choose **Start Learning**.

1. In **MFA fatigue**, read the scenario objective and safety notice. The exercise uses prewritten observations from a synthetic identity provider.
2. Select **Inspect baseline**. Expand an event and compare the outcome and authentication method. The baseline uses successful FIDO2 records.
3. Select **Continue to replay**, then **Replay safe events**. Look for one alert and three records labeled **Alert evidence**.
4. Open the **Evidence timeline**. Expand a denied prompt and read the user, challenge ID and evidence reference. Compare all three prompt timestamps and see how they fit in five minutes. Use **JSON** or **CSV** to export the run.
5. Return to the lesson, select **Replay & evidence** and **Replay noisy events**. Find duplicated challenge IDs and the approved enrollment record. Explain why counting raw denials would overstate the signal.
6. Continue to **Response** and note when to verify the user or revoke a session. Take the knowledge check and select **Mark as completed** after reviewing feedback.
7. Open **Learning Progress** and download a report. Use **Technique Explorer** or follow a [curriculum](curricula/README.md) to select the next exercise.

Expected evidence for the bundled examples is described in the [MFA case study](case-studies/02-mfa-fatigue.md). [Deployment issues](TROUBLESHOOTING.md)
