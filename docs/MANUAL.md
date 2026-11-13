# Manual — catalogo_tecnico
Procedimentos e lições só deste projeto. Regra geral fica nas skills (conduta §E1).

## Dados
- 2026-11-13 · Ficha técnica individual do perfil prevalece sobre o YAML e planilhas; exceções SS-002 (vale o YAML) e FE-0207 (área 274.43) · origem: demanda 351
- 2026-11-13 · Premissas de src/data/estrutural.yaml são preliminares até validação do Coordenador de Produção; nada de gráfico de pressão publicado antes · origem: demanda 351

## Build e publicação
- 2026-11-13 · docs/ é gerado por python src/build.py e nunca é editado à mão · origem: demanda 351
- 2026-11-13 · Push em main dispara o deploy em https://catalogo.solucaointeligentes.com; GitHub Pages só redireciona · origem: demanda 351

## Governança
- 2026-11-13 · Motor gov_engine roda só por .venv\Scripts\python.exe com a pasta atual em C:\GITHUB\GOV_IA_CORE · origem: demanda 351
- 2026-11-13 · Número do próximo passo: conferir gov_passos do projeto, não só o ROTEIRO (o 109 saiu repetido: P=110 e P=158) · origem: HIST_2026-11-13_a_2026-11-13_catalogo_tecnico_projnovo-regularizacao-a7.md#P9
