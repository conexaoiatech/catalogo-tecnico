# DXF pendentes para o gráfico de pressão

Perfis estruturais (`perfis_estruturais` das categorias) sem `modulo_wx_mm3` (ou sem o módulo do eixo usado). Gerado por `scripts/grafico_pressao.py`.

Regras do DXF limpo (as mesmas validadas no SS-108):

- só o contorno da seção (sem cotas, textos, eixos, hachuras nem outros perfis);
- unidades em mm, escala 1:1 (o `INSUNITS` do arquivo pode estar errado; vale o desenho em mm);
- na orientação da ficha (se girado ou espelhado, avisar para ajustar `--orient`);
- furos reais como contornos internos fechados;
- contornos fechados, sem lacunas maiores que alguns centésimos de mm.

| Perfil | Sistemas (estrutural) | Caminho esperado | DXF existe? |
|---|---|---|---|
| SS-001 | portas-minimalistas, sacada | `cad-fonte\ARQUIVOS\CALCULO\SS-001.dxf` | não |
| SS-002 | sacada | `cad-fonte\ARQUIVOS\CALCULO\SS-002.dxf` | não |
| SS-003 | sacada | `cad-fonte\ARQUIVOS\CALCULO\SS-003.dxf` | não |
| SS-004 | portas-minimalistas, portas-robustas | `cad-fonte\ARQUIVOS\CALCULO\SS-004.dxf` | não |
| SS-005 | portas-minimalistas | `cad-fonte\ARQUIVOS\CALCULO\SS-005.dxf` | não |
| SS-010 | portas-minimalistas, sacada | `cad-fonte\ARQUIVOS\CALCULO\SS-010.dxf` | não |
| SS-016 | pele-vidro, portas-robustas | `cad-fonte\ARQUIVOS\CALCULO\SS-016.dxf` | não |
| SS-017 | pele-vidro, portas-robustas | `cad-fonte\ARQUIVOS\CALCULO\SS-017.dxf` | não |
| SS-020 | portas-minimalistas | `cad-fonte\ARQUIVOS\CALCULO\SS-020.dxf` | não |
| SS-021 | portas-minimalistas | `cad-fonte\ARQUIVOS\CALCULO\SS-021.dxf` | não |
| SS-022 | portas-minimalistas | `cad-fonte\ARQUIVOS\CALCULO\SS-022.dxf` | não |
| SS-023 | portas-minimalistas | `cad-fonte\ARQUIVOS\CALCULO\SS-023.dxf` | não |
| SS-024 | pele-vidro, portas-robustas | `cad-fonte\ARQUIVOS\CALCULO\SS-024.dxf` | não |
| SS-027 | pele-vidro | `cad-fonte\ARQUIVOS\CALCULO\SS-027.dxf` | não |
| SS-028 | pele-vidro | `cad-fonte\ARQUIVOS\CALCULO\SS-028.dxf` | não |
| F98 | portas-minimalistas, portas-robustas | `cad-fonte\ARQUIVOS\CALCULO\F98.dxf` | não |
