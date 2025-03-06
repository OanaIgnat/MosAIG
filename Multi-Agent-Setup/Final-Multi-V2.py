# import logging
# import os
# from crewai import Agent, Task, Crew, LLM

# # ✅ Set API Key Manually or from Environment Variable
# os.environ["TOGETHERAI_API_KEY"] = ""  # Replace with actual key

# # ✅ Define LLM for Together AI
# llm = LLM(
#     model="together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
#     base_url="https://api.together.xyz/v1",
#     api_key=os.getenv("TOGETHERAI_API_KEY")
# )

# # ✅ Define Two Agents (Persona & Place)
# persona_agent = Agent(
#     role="Persona Expert",
#     goal="Provide culturally rich descriptions of attire.",
#     backstory="Expert in cultural traditions and attire details.",
#     llm=llm,
#     verbose=True
# )

# place_agent = Agent(
#     role="Place Expert",
#     goal="Describe famous landmarks vividly.",
#     backstory="Knows famous landmarks and their environmental elements.",
#     llm=llm,
#     verbose=True
# )

# # ✅ Define Tasks for Both Agents
# persona_task = Task(
#     description="Describe traditional attire of an Indian person.",
#     agent=persona_agent,
#     expected_output="Culturally rich attire description under 25 words."
# )

# place_task = Task(
#     description="Describe the architectural beauty of the Eiffel Tower.",
#     agent=place_agent,
#     expected_output="Vivid architectural description under 25 words."
# )

# # ✅ Create a Crew and Run Tasks
# crew = Crew(agents=[persona_agent, place_agent], tasks=[persona_task, place_task], verbose=True)
# result = crew.kickoff()

# # ✅ Print Final Output
# print("\nFinal Output:")
# print("=" * 50)
# print(result)
# print("=" * 50)


# import logging
# import os
# from crewai import Agent, Task, Crew, LLM
# from datetime import datetime

# # Create a file name with timestamp
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# output_file = f"crew_output_{timestamp}.txt"

# # Initialize LLM and agents
# os.environ["TOGETHERAI_API_KEY"] = ""  # Replace with actual key

# llm = LLM(
#     model="together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
#     base_url="https://api.together.xyz/v1",
#     api_key=os.getenv("TOGETHERAI_API_KEY")
# )

# persona_agent = Agent(
#     role="Persona Expert",
#     goal="Provide culturally rich descriptions of attire.",
#     backstory="Expert in cultural traditions and attire details.",
#     llm=llm,
#     verbose=True
# )

# place_agent = Agent(
#     role="Place Expert",
#     goal="Describe famous landmarks vividly.",
#     backstory="Knows famous landmarks and their environmental elements.",
#     llm=llm,
#     verbose=True
# )

# persona_task = Task(
#     description="Describe traditional attire of an Indian person.",
#     agent=persona_agent,
#     expected_output="Culturally rich attire description under 25 words."
# )

# place_task = Task(
#     description="Describe the architectural beauty of the Eiffel Tower.",
#     agent=place_agent,
#     expected_output="Vivid architectural description under 25 words."
# )

# # Create and run crew
# crew = Crew(
#     agents=[persona_agent, place_agent], 
#     tasks=[persona_task, place_task], 
#     verbose=True
# )

# result = crew.kickoff()

# # Write only the result string to file
# with open(output_file, 'w') as f:
#     f.write(str(result).strip())

# print(f"\nExecution complete. Results have been written to: {output_file}")


import os
from crewai import Agent, Task, Crew, LLM

class PromptCrewManager:
    def __init__(self):
        # Initialize LLM with Together AI
        self.llm = LLM(
            model="together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            base_url="https://api.together.xyz/v1",
            api_key=os.getenv("TOGETHERAI_API_KEY")
        )

    def create_agents(self):
        # Create agents with dynamic personas
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

        # Round 1 Tasks
        persona_task = Task(
            description=f"""
            You are a {nationality} person from {country} who knows the culture of this country well.
            Provide a visual description of culturally appropriate traditional clothing, accessories, and colors, for the {nationality} person.
            Focus on specific materials, key cultural patterns, and symbolic colors.
            Your response must be under 25 words.
            """,
            agent=agents['persona_agent'],
            expected_output="Culturally rich attire description under 25 words."
        )

        place_task = Task(
            description=f"""
            You are a person who has visited {place} many times and know this landmark well.
            Provide a visual description of its architectural features, colors, and environmental details.
            Your response must be under 25 words.
            """,
            agent=agents['place_agent'],
            expected_output="Detailed place description under 25 words."
        )

        age_gender_task = Task(
            description=f"""
            You are a {age_gender_combined} and can describe traits of this person well.
            Provide a visual description of attire, accessories, and physical details.
            Focus on skin, body, hair texture, and accessories.
            Your response must be under 25 words.
            """,
            agent=agents['age_gender_agent'],
            expected_output="Detailed age-gender description under 25 words."
        )

        # Feedback Questions (Round 2)
        feedback_questions = [
            f"How would a person's clothing harmonize with the colors of {place}?",
            f"What attire adjustments could reflect age-appropriate traits for a {nationality} {age_gender_combined}?",
            f"What visual elements of {place} would complement the persona's attire?",
            f"Any additional visual traits should a {age_gender_combined} of {nationality} nationality from {country} have?"
        ]

        persona_feedback_task = Task(
            description=f"Enhance the persona description by addressing: '{feedback_questions[0]}'.",
            agent=agents['persona_agent'],
            context=[persona_task],
            expected_output="Enhanced persona description under 25 words."
        )

        place_feedback_task = Task(
            description=f"Enhance the place description by addressing: '{feedback_questions[2]}'.",
            agent=agents['place_agent'],
            context=[place_task],
            expected_output="Enhanced place description under 25 words."
        )

        age_gender_feedback_task = Task(
            description=f"Enhance the age-gender description by addressing: '{feedback_questions[1]}'.",
            agent=agents['age_gender_agent'],
            context=[age_gender_task],
            expected_output="Enhanced age-gender description under 25 words."
        )

        # Summarization Task
        summarization_task = Task(
            description=f"Give a final prompt in a single one line under 48 words and under 77 tokens strictly. Ensure the words {nationality}, {age_gender_combined}, and 'smile' of the person and other descriptions with the {place} background are mentioned explicitly in the final prompt.",
            agent=agents['summarizer_agent'],
            context=[persona_feedback_task, place_feedback_task, age_gender_feedback_task],
            expected_output="Single-line text-to-image prompt under 48 words and specifically under 77 tokens strictly."
        )

        return [
            persona_task,
            place_task,
            age_gender_task,
            persona_feedback_task,
            place_feedback_task,
            age_gender_feedback_task,
            summarization_task
        ]

    def generate_prompt(self, inputs):
        try:
            print("Initializing text-to-image prompt generation...")

            # Create agents and tasks
            agents = self.create_agents()
            tasks = self.create_tasks(agents, inputs)

            # Create a crew and execute the tasks
            crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                verbose=True
            )
            print("Starting the task execution...")
            result = crew.kickoff()
            return result

        except Exception as e:
            print(f"Error during prompt generation: {e}")
            return None

def main():
    try:
        # Set your API key here
        together_api_key = ""  # <-- Enter your Together AI API key here
        os.environ["TOGETHERAI_API_KEY"] = together_api_key

        if not together_api_key:
            raise ValueError("Please enter your Together AI API key in the code.")

        # Initialize the system
        manager = PromptCrewManager()

        # Example input
        inputs = {
            "country": "America",
            "nationality": "American",
            "age": "Old",
            "gender": "Female",
            "place": "Taj Mahal",
            "age_gender_combined": "Old Woman"
        }

        # Generate the final prompt
        final_prompt = manager.generate_prompt(inputs)

        if final_prompt:
            # Extract only the summarizer's final output
            summarizer_output = str(final_prompt).split("Prompt Finalizer:")[-1].strip()
            # Write only the final summary to file
            with open('output.txt', 'w') as f:
                f.write(summarizer_output)
            print("\nFinal prompt has been written to: output.txt")
        else:
            print("Failed to generate prompt.")

    except KeyboardInterrupt:
        print("Execution interrupted by user.")
    except Exception as e:
        print(f"Critical error in main: {e}")

if __name__ == "__main__":
    main()
