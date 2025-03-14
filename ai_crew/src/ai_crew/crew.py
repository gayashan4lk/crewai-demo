from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AiCrew():
	"""AiCrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	anthropic_model_haiku = f"anthropic/{os.getenv('ANTHROPIC_MODEL_HAIKU', 'claude-3-5-haiku-latest')}"
	anthropic_model_sonnet = f"anthropic/{os.getenv('ANTHROPIC_MODEL_SONNET', 'claude-3-7-sonnet-latest')}"

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		researcher_llm = LLM(model=self.anthropic_model_haiku, temperature=0.5)
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			llm=researcher_llm
		)

	@agent
	def reporting_analyst(self) -> Agent:
		reporting_analyst_llm = LLM(model=self.anthropic_model_haiku, temperature=0.5)
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			llm=reporting_analyst_llm
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AiCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge
		manager_llm = LLM(model=self.anthropic_model_sonnet, temperature=0.2)

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			manager_llm=manager_llm,
			verbose=True,
		)
