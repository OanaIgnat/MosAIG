import os
import pandas as pd
from crewai import Agent, Task, Crew, LLM

class PromptCrewManager:
    def __init__(self):
        self.llm = LLM(
            model="together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            base_url="https://api.together.xyz/v1",
            api_key=os.getenv("TOGETHERAI_API_KEY")
        )

    def create_agents(self):
        persona_agent = Agent(
            role="Persona Expert",
            goal="Provide culturally rich descriptions of attire and accessories.",
            backstory="You are an expert in cultural traditions and attire details.",
            llm=self.llm,
            verbose=True
        )

        place_agent = Agent(
            role="Place Expert",
            goal="Provide vivid descriptions of architectural and environmental elements.",
            backstory="You have extensive knowledge of landmarks and their visual details.",
            llm=self.llm,
            verbose=True
        )

        age_gender_agent = Agent(
            role="Age-Gender Visual Expert",
            goal="Provide detailed descriptions of physical traits, attire, and accessories for specific demographics.",
            backstory="You specialize in visually descriptive traits based on age and gender.",
            llm=self.llm,
            verbose=True
        )

        summarizer_agent = Agent(
            role="Prompt Finalizer",
            goal="After studying all the descriptions give a single line text-to-image prompt.",
            backstory="You excel at crafting precise and coherent visual prompts, under 48 words and specifically under 77 tokens strictly.",
            llm=self.llm,
            verbose=True
        )

        return {
            'persona_agent': persona_agent,
            'place_agent': place_agent,
            'age_gender_agent': age_gender_agent,
            'summarizer_agent': summarizer_agent
        }

    def create_tasks(self, agents, input_data):
        country = input_data['country']
        nationality = input_data['nationality']
        place = input_data['place']
        age_gender_combined = input_data['age_gender_combined']

        persona_task = Task(
            description=f"You are a {nationality} from {country}. Describe their traditional attire and accessories in under 25 words.",
            agent=agents['persona_agent'],
            expected_output="Culturally rich attire description under 25 words."
        )

        place_task = Task(
            description=f"Describe the visual aspects of {place} in under 25 words.",
            agent=agents['place_agent'],
            expected_output="Detailed place description under 25 words."
        )

        age_gender_task = Task(
            description=f"Describe a {age_gender_combined} including attire, accessories, and physical traits in under 25 words.",
            agent=agents['age_gender_agent'],
            expected_output="Detailed age-gender description under 25 words."
        )

        summarization_task = Task(
            description=f"Provide a single one-line prompt under 48 words and 77 tokens including '{nationality}', '{age_gender_combined}', and '{place}'.",
            agent=agents['summarizer_agent'],
            context=[persona_task, place_task, age_gender_task],
            expected_output="Single-line text-to-image prompt under 48 words."
        )

        return [persona_task, place_task, age_gender_task, summarization_task]

    def generate_prompt(self, inputs):
        try:
            agents = self.create_agents()
            tasks = self.create_tasks(agents, inputs)
            crew = Crew(agents=list(agents.values()), tasks=tasks, verbose=True)
            return crew.kickoff()
        except Exception as e:
            print(f"Error during prompt generation: {e}")
            return None

def process_excel():
    try:
        file_path = "outlet.xlsx"
        df = pd.read_excel(file_path, engine='openpyxl')  # ✅ Read with UTF-8 support

        with open('output.txt', 'a', encoding='utf-8') as output_file:  # ✅ Append mode & UTF-8 encoding
            manager = PromptCrewManager()

            for index, row in df.iterrows():
                inputs = {
                    "country": row["country"],
                    "nationality": row["nationality"],
                    "place": row["place"],
                    "age_gender_combined": row["age_gender_combined"]
                }

                final_prompt = manager.generate_prompt(inputs)
                if final_prompt:
                    summarizer_output = str(final_prompt).split("Prompt Finalizer:")[-1].strip()

                    # ✅ Append to TXT file and save instantly
                    output_file.write(summarizer_output + "\n")
                    output_file.flush()  # ✅ Force save immediately

                    # ✅ Update Excel instantly
                    df.at[index, "Prompt"] = summarizer_output
                    df.to_excel(file_path, index=False, engine='openpyxl')  # ✅ Save immediately

                    # ✅ Print completion message
                    print(f"Row-{index + 1} Done!!")

        print("\n✅ All prompts have been saved to output.txt and updated in outlet.xlsx!")

    except Exception as e:
        print(f"❌ Critical error in processing Excel: {e}")

if __name__ == "__main__":
    together_api_key = ""  # <-- Enter your Together AI API key here # USING LLAMA-3.1-8B (OPEN SOURCE MODEL !!)
    os.environ["TOGETHERAI_API_KEY"] = together_api_key
    process_excel()

# import os
# from crewai import Agent, Task, Crew
# from langchain.chat_models import ChatOpenAI

# # Set environment variables for API keys
# os.environ["OPENAI_API_KEY"] = "" #USING OPENAI-API GPT-4 (NOT OPEN SOURCE)

# class PromptCrewManager:
#     def __init__(self):
#         try:
#             # Initialize ChatOpenAI with environment variable for API key
#             self.llm = ChatOpenAI(
#                 model_name="gpt-4",
#                 openai_api_key=os.getenv("OPENAI_API_KEY")
#             )
#         except Exception as e:
#             print(f"Failed to initialize LLM: {e}")
#             raise

#     def create_agents(self):
#         # Create agents with dynamic personas
#         persona_agent = Agent(
#             role="Persona Expert",
#             goal="Provide culturally rich descriptions of attire and accessories.",
#             backstory="You are an expert in cultural traditions and attire details.",
#             llm=self.llm,
#             verbose=True
#         )

#         place_agent = Agent(
#             role="Place Expert",
#             goal="Provide vivid descriptions of architectural and environmental elements.",
#             backstory="You have extensive knowledge of landmarks and their visual details.",
#             llm=self.llm,
#             verbose=True
#         )

#         age_gender_agent = Agent(
#             role="Age-Gender Visual Expert",
#             goal="Provide detailed descriptions of physical traits, attire, and accessories for specific demographics.",
#             backstory="You specialize in visually descriptive traits based on age and gender.",
#             llm=self.llm,
#             verbose=True
#         )

#         summarizer_agent = Agent(
#             role="Prompt Finalizer",
#             goal="After studying all the descriptions give a single line text-to-image prompt.",
#             backstory="You excel at crafting precise  and coherent visual prompts, under 48 words and specifially under 77 tokens strictly.",
#             llm=self.llm,
#             verbose=True
#         )

#         return {
#             'persona_agent': persona_agent,
#             'place_agent': place_agent,
#             'age_gender_agent': age_gender_agent,
#             'summarizer_agent': summarizer_agent
#         }

#     def create_tasks(self, agents, input_data):
#         country = input_data['country']
#         nationality = input_data['nationality']
#         place = input_data['place']
#         age_gender_combined = input_data['age_gender_combined']

#         # Round 1 Tasks
#         persona_task = Task(
#             description=f"""
#             You are a {nationality} person from {country} who knows the culture of this country well.
#             Provide a visual description of culturally appropriate traditional clothing, accessories, and colors, for the {nationality} person.
#             Focus on specific materials, key cultural patterns, and symbolic colors.
#             Your response must be under 25 words.
#             """,
#             agent=agents['persona_agent'],
#             expected_output="Culturally rich attire description under 25 words."
#         )

#         place_task = Task(
#             description=f"""
#             You are a person who has visited {place} many times and know this landmark well.
#             Provide a visual description of its architectural features, colors, and environmental details.
#             Your response must be under 25 words.
#             """,
#             agent=agents['place_agent'],
#             expected_output="Detailed place description under 25 words."
#         )

#         age_gender_task = Task(
#             description=f"""
#             You are a {age_gender_combined} and can describe traits of this person well.
#             Provide a visual description of attire, accessories, and physical details.
#             Focus on skin, body, hair texture, and accessories.
#             Your response must be under 25 words.
#             """,
#             agent=agents['age_gender_agent'],
#             expected_output="Detailed age-gender description under 25 words."
#         )

#         # Feedback Questions (Round 2)
#         feedback_questions = [
#             f"How would a person's clothing harmonize with the colors of {place}?",
#             f"What attire adjustments could reflect age-appropriate traits for a {nationality} {age_gender_combined}?",
#             f"What visual elements of {place} would complement the persona's attire?",
#             f"Any additional visual traits should a {age_gender_combined} of {nationality} nationality from {country} have?"
#         ]

#         persona_feedback_task = Task(
#             description=f"Enhance the persona description by addressing: '{feedback_questions[0]}'.",
#             agent=agents['persona_agent'],
#             context=[persona_task],
#             expected_output="Enhanced persona description under 25 words."
#         )

#         place_feedback_task = Task(
#             description=f"Enhance the place description by addressing: '{feedback_questions[2]}'.",
#             agent=agents['place_agent'],
#             context=[place_task],
#             expected_output="Enhanced place description under 25 words."
#         )

#         age_gender_feedback_task = Task(
#             description=f"Enhance the age-gender description by addressing: '{feedback_questions[1]}'.",
#             agent=agents['age_gender_agent'],
#             context=[age_gender_task],
#             expected_output="Enhanced age-gender description under 25 words."
#         )

#         # Summarization Task
#         summarization_task = Task(
#             description=f"Give a final prompt in a single one line under 48 words and under 77 tokens strictly. Ensure the words {nationality}  and {age_gender_combined} of the person and other descriptions with the {place} background are mentoned explicitly in the final prompt.",
#             agent=agents['summarizer_agent'],
#             context=[persona_feedback_task, place_feedback_task, age_gender_feedback_task],
#             expected_output="Single-line text-to-image prompt under 48 words and specifically under 77 tokens strictly."
#         )

#         return [
#             persona_task,
#             place_task,
#             age_gender_task,
#             persona_feedback_task,
#             place_feedback_task,
#             age_gender_feedback_task,
#             summarization_task
#         ]

#     def generate_prompt(self, inputs):
#         try:
#             print("Initializing text-to-image prompt generation...")

#             # Create agents and tasks
#             agents = self.create_agents()
#             tasks = self.create_tasks(agents, inputs)

#             # Create a crew and execute the tasks
#             crew = Crew(
#                 agents=list(agents.values()),
#                 tasks=tasks,
#                 verbose=True
#             )
#             print("Starting the task execution...")
#             result = crew.kickoff(inputs=inputs)
#             return result

#         except Exception as e:
#             print(f"Error during prompt generation: {e}")
#             return None


# def main():
#     try:
#         # Ensure API key is set
#         if not os.getenv("OPENAI_API_KEY"):
#             raise ValueError("OPENAI_API_KEY environment variable is not set.")

#         # Initialize the system
#         manager = PromptCrewManager()

#         # Example input
#         inputs = {
#             "country": "India",
#             "nationality": "Indian",
#             "age": "Child",
#             "gender": "Female",
#             "place": "Cologne Cathedral",
#             "age_gender_combined": "Young Girl"
#         }

#         # Generate the final prompt
#         final_prompt = manager.generate_prompt(inputs)

#         if final_prompt:
#             print("\nFinal Prompt:")
#             print("=" * 50)
#             print(final_prompt)
#             print("=" * 50)
#         else:
#             print("Failed to generate prompt.")

#     except KeyboardInterrupt:
#         print("Execution interrupted by user.")
#     except Exception as e:
#         print(f"Critical error in main: {e}")


# if __name__ == "__main__":
#     main()
