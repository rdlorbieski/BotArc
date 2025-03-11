from bots.BaseBot import BaseBot
from apis.OpenAIClient import OpenAIClient
import sympy as sp
import numpy as np
import random

class EquationOptimizerBot(BaseBot):
    def __init__(self, config):
        super().__init__(config)
        self.openai_client = OpenAIClient(api_key=config.gpt_key, model="gpt-4o")

    def process_message(self, message=None):
        """Tenta otimizar uma equação matemática. Se não entender, usa o GPT."""

        try:
            # Verifica se a entrada parece uma equação matemática
            if not any(char.isdigit() or char in "+-*/^=()" for char in message):
                return "⚠️ Parece que sua entrada não é uma equação matemática."

            # Se for um problema de otimização, resolvemos com Algoritmo Genético
            resultado = self.optimize_equation(message)
            if resultado:
                return resultado

            # Se não entender, pede para o GPT reformular a pergunta
            prompt_reformulacao = f"Reformule esta pergunta para um bot de otimização entender melhor: '{message}'"
            reformulado = self.openai_client.send_request(prompt=prompt_reformulacao)

            # Tenta otimizar a equação reformulada
            resultado = self.optimize_equation(reformulado)
            if resultado:
                return resultado

            # Se ainda não entender, passa direto para o GPT resolver
            prompt_solucao = f"Resolva a seguinte equação ou problema de otimização:\n\n{message}"
            return self.openai_client.send_request(prompt=prompt_solucao)

        except Exception as e:
            return f"❌ Erro ao processar a mensagem: {str(e)}"

    def optimize_equation(self, equation):
        """Usa Algoritmos Genéticos para encontrar o valor ótimo de uma função."""
        try:
            x = sp.Symbol("x")

            # Tenta converter a string para uma expressão matemática
            try:
                expr = sp.sympify(equation)
            except Exception:
                return None  # Se não conseguir converter, deixa o GPT tentar

            # Verifica se a equação contém apenas a variável 'x'
            if len(expr.free_symbols) != 1 or x not in expr.free_symbols:
                return None  # Se tiver mais de uma variável, deixa o GPT resolver

            # Função para avaliar a expressão para um dado valor de x
            def func(value):
                try:
                    return float(expr.subs(x, value))
                except:
                    return float("inf")  # Retorna infinito em caso de erro

            # Parâmetros do Algoritmo Genético
            pop_size = 20  # Tamanho da população
            generations = 100  # Número de gerações
            mutation_rate = 0.1  # Taxa de mutação
            range_min, range_max = -10, 10  # Intervalo de busca

            # Inicializa população aleatória
            population = [random.uniform(range_min, range_max) for _ in range(pop_size)]

            for _ in range(generations):
                # Avaliação (fitness)
                fitness = [func(ind) for ind in population]

                # Se todos os valores forem infinitos, aborta
                if all(np.isinf(fitness)):
                    return "⚠️ Não foi possível otimizar esta função."

                # Seleção dos melhores (elitismo)
                sorted_indices = np.argsort(fitness)  # Ordena os índices
                best_individuals = [population[i] for i in sorted_indices[: pop_size // 2]]

                # Cruzamento (crossover)
                offspring = []
                while len(offspring) < pop_size - len(best_individuals):
                    p1, p2 = random.sample(best_individuals, 2)
                    child = (p1 + p2) / 2  # Média aritmética como crossover simples
                    offspring.append(child)

                # Mutação
                for i in range(len(offspring)):
                    if random.random() < mutation_rate:
                        offspring[i] += random.uniform(-1, 1)  # Pequena variação aleatória

                # Atualiza a população
                population = best_individuals + offspring

            # Melhor solução encontrada
            best_solution = min(population, key=func)
            best_value = func(best_solution)

            return f"🔬 Melhor solução encontrada: x = {best_solution:.4f}, f(x) = {best_value:.4f}"

        except Exception as e:
            return None  # Se der erro, deixa o GPT tentar
