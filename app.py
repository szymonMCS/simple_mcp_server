import gradio as gr
import asyncio
from mcp_client import MCPOpenAIClient
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class App:

    def __init__(self):
        self.mcp_client = MCPOpenAIClient()
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    async def ask_with_mcp(self, question: str) -> str:
        """Ask a question using MCP (with tool access)"""
        try:
            await self.mcp_client.connect_to_mcp_server()
            result = await self.mcp_client.run_agent(question)
            return result
        except Exception as e:
            return f"Error: {str(e)}\n\nMake sure the MCP server is properly configured."

    def ask_openai(self, question: str) -> str:
        """Ask a question to OpenAI (without tools)"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": question}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


def create_ui():
    app = App()

    with gr.Blocks(title="MCP Date Check", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# MCP Date Check Demo")
        gr.Markdown("""
        This app demonstrates an MCP (Model Context Protocol) server with a custom date tool.

        **With MCP Tools**: The agent can call the `get_current_date` tool to get today's date.

        **Without MCP Tools**: The agent responds without access to tools (may hallucinate dates).
        """)

        with gr.Row():
            with gr.Column():
                gr.Markdown("### With MCP Tools")
                question_with_mcp = gr.Textbox(
                    label="Question",
                    placeholder="What is today's date?",
                    value="What is today's date?"
                )
                btn_with_mcp = gr.Button("Ask with MCP", variant="primary")
                output_with_mcp = gr.Textbox(label="Response", lines=5)

            with gr.Column():
                gr.Markdown("### Without MCP Tools")
                question_without_mcp = gr.Textbox(
                    label="Question",
                    placeholder="What is today's date?",
                    value="What is today's date?"
                )
                btn_without_mcp = gr.Button("Ask OpenAI")
                output_without_mcp = gr.Textbox(label="Response", lines=5)

        btn_with_mcp.click(
            fn=lambda q: asyncio.run(app.ask_with_mcp(q)),
            inputs=question_with_mcp,
            outputs=output_with_mcp
        )
        btn_without_mcp.click(
            fn=app.ask_openai,
            inputs=question_without_mcp,
            outputs=output_without_mcp
        )

    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )