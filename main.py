import pygame
import sys
import json
import os # Importante para verificar se o arquivo de save existe
import random
from settings import LARGURA, ALTURA, FPS, COR_CEU_BAIXO, COR_CHAO, COR_MOEDA
from engine.player import Jogador
from engine.obstacles import Moeda, Obstaculo

class Game:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Homebound - Estilo Mario")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Arial", 25, bold=True)
        
        # Estados
        self.pausado = False
        self.som_ativo = True
        self.score = 0
        self.recorde = self.carregar_dados()

        # Objetos
        self.player = Jogador()
        self.grupo_player = pygame.sprite.GroupSingle(self.player)
        from engine.obstacles import Moeda, Obstaculo # No topo do arquivo

        # Dentro do def __init__(self):
        self.moedas_total = 0      # Pontuação atual (moedas)
        self.tempo_partida = 0     # Tempo da partida atual
        self.recorde_tempo = 0
        self.cor_recorde = (200, 200, 200)

        # Dentro do self.__init__:
        self.grupo_moedas = pygame.sprite.Group()
        self.grupo_obstaculos = pygame.sprite.Group()

        # Vamos criar algumas moedas de teste no mapa
        for i in range(10):
            x_aleatorio = random.randint(200, 900)
            nova_moeda = Moeda(x_aleatorio, 450)
            self.grupo_moedas.add(nova_moeda)

    def carregar_dados(self):
        # Verifica se o arquivo existe antes de tentar ler (Evita bugs)
        if os.path.exists("save.json"):
            try:
                with open("save.json", "r") as f:
                    return json.load(f).get("high_score", 0)
            except:
                return 0
        return 0

    def salvar_dados(self):
        novo_recorde = max(self.tempo_partida, self.recorde_tempo)
        with open("save.json", "w") as f:
            json.dump({"high_score": novo_recorde}, f)

    def mostrar_hud(self):
        txt_pontos = self.fonte.render(f"PONTOS: {int(self.score)}", True, (255, 255, 255))
        txt_recorde = self.fonte.render(f"RECORDE: {int(self.recorde_tempo)}", True, self.cor_recorde)
        self.tela.blit(txt_pontos, (20, 20))
        self.tela.blit(txt_recorde, (20, 60))
        
        if self.pausado:
            # Fundo semitransparente para o pause (deixa o jogo "bonito")
            overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) 
            self.tela.blit(overlay, (0,0))
            
            txt_pause = self.fonte.render("JOGO PAUSADO - Aperte P para Voltar", True, (255, 255, 255))
            self.tela.blit(txt_pause, (LARGURA//2 - 180, ALTURA//2))

            txt_moedas = self.fonte.render(f"MOEDAS: {int(self.score // 100)}", True, COR_MOEDA)
            self.tela.blit(txt_moedas, (20, 80))

            # Mostra as moedas coletadas na partida atual
            txt_moedas = self.fonte.render(f"PONTOS: {int(self.moedas_total)}", True, (255, 255, 255))
    
            # Mostra o tempo da partida atual vs o Recorde de tempo
            # HI (High Score) baseado no tempo
            tempo_exibir = max(self.tempo_partida, self.recorde_tempo)
            txt_recorde = self.fonte.render(f"RECORDE: {int(tempo_exibir)}", True, (200, 200, 200))
    
            self.tela.blit(txt_pontos, (20, 20))
            self.tela.blit(txt_recorde, (20, 60))

    def rodar(self): # Aqui está a função que você chama com ()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.salvar_dados()
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: 
                        self.pausado = not self.pausado
                    if event.key == pygame.K_m: 
                        self.som_ativo = not self.som_ativo
                    if event.key == pygame.K_ESCAPE:
                        self.salvar_dados()
                        pygame.quit()
                        sys.exit()

            if not self.pausado:
                self.grupo_player.update()
            # 1. Coletar Moedas
                colisoes_moedas = pygame.sprite.spritecollide(self.player, self.grupo_moedas, True)
            if colisoes_moedas:
                self.score += 10 # Cada moeda vale 10 pontos
            # Se self.som_ativo: tocar_som_moeda()
            self.recorde_tempo += 1

            if self.recorde_tempo > 0 and self.recorde_tempo % 1000 == 0:
                self.cor_recorde = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
            # 2. Coleta de Moedas (Pontos do Jogo)
            colisoes = pygame.sprite.spritecollide(self.player, self.grupo_moedas, True)
            if colisoes:
                self.moedas_total += 10 # Cada moeda agora vale 10

            # 2. Bater em Obstáculos (Reset)
            if pygame.sprite.spritecollide(self.player, self.grupo_obstaculos, False):
                self.salvar_dados()
                self.reiniciar_jogo() 

            # Camadas de Desenho
            self.tela.fill(COR_CEU_BAIXO)
            pygame.draw.rect(self.tela, COR_CHAO, (0, 500, LARGURA, 100))
            
            self.grupo_player.draw(self.tela)
            self.mostrar_hud()
            self.grupo_moedas.draw(self.tela)
            pygame.display.flip()
            self.relogio.tick(FPS)

if __name__ == "__main__":
    meu_jogo = Game()
    meu_jogo.rodar() # Agora com parênteses para executar a função!

    def reiniciar_jogo(self):
        self.salvar_dados()
    # Quando morre, os pontos voltam para 0
        self.score = 0 
        self.tempo_partida = 0
    # Recarrega o recorde do arquivo
        self.recorde_tempo = self.carregar_dados()
    # Reposiciona o player
        self.player.rect.midbottom = (100, 500)