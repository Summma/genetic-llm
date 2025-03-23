class Prompt:
    def __init__(self, prompt_name: str) -> None:
        self.prompt, self.function_start, self.function_end = self.get_prompt(prompt_name)
        self.function_start = self.function_start - 2
        self.function_end = self.function_end - 1

    def substitute_function(self, new_func: str) -> tuple[str, int, int]:
        prompt_list = self.prompt.split("\n")
        out_prompt_list = prompt_list[:self.function_start] + new_func.split("\n") + prompt_list[self.function_end:]

        return ("\n".join(out_prompt_list), self.function_start, self.function_start + len(new_func.split("\n")))

    def change_function(self, new_func: str) -> None:
        prompt, start, end = self.substitute_function(new_func)

        self.prompt = prompt
        self.function_start = start
        self.function_end = end

    @staticmethod
    def get_prompt(file_name: str) -> tuple[str, int, int]:
        with open(f"prompts/{file_name}", "r") as f:
            lines = f.readlines()
            info, text = lines[0], "".join(lines[1:])

            start, end = map(int, info.split())
            return (text, start, end)

    def __repr__(self):
        return self.prompt

if __name__ == "__main__":
    prompt = Prompt("symbolic_prompt.txt")
    # prompt, start, end = prompt.substitute_function("def test():\n    print(\"Hello World\")")
    prompt.change_function("def test():\n    print(\"Hello World\")")

    print(prompt)
