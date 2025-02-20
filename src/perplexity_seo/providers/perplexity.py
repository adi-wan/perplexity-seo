from askui import VisionAgent
import webbrowser
import pyperclip

class Perplexity:
    def query(self, prompt: str) -> str:
        webbrowser.get("chrome").open("https://www.perplexity.ai?zoom=4")  # Windows
        with VisionAgent() as agent:
            agent.act(f"Ask \"{prompt}\" and copy the answer to the clipboard by clicking on 'Stellen Sie Ihre Frage...' or 'Ask anything...', then entering the prompt and clicking on 'Enter'. You are done when you see the \"Teilen\" or \"Share\" button in the top right hand corner. Finish with clicking a word in the answer afterwards.")
            n = 100
            while n > 0: 
                agent.keyboard("pagedown")
                n -= 1
            agent.act("Click on the copy icon button to copy the content to clipboard which is right of the thumbs down and thumbs up buttons")
            return pyperclip.paste()
