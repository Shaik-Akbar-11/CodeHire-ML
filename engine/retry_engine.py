class RetryEngine:

    def __init__(self):
        pass

    def improve_prompt(
        self,
        prompt,
        errors
    ):

        feedback = "\n\nThe previous question was rejected.\n"

        feedback += "Correct these mistakes:\n"

        for error in errors:
            feedback += f"- {error}\n"

        feedback += """

Generate a COMPLETELY NEW question.

Do NOT modify the previous question.

Do NOT repeat previous mistakes.

Return ONLY JSON.
"""

        return prompt + feedback