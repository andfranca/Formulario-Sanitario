from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="SIVIG - Sistema Integrado de Vigilância Sanitária")

# Armazenamento em memória conforme regra (sem banco de dados)
registros = []
registro_id_counter = 1

class RegistroCreate(BaseModel):
    nome: str
    passaporte: str
    telefone: str
    email: str
    pais: str
    voo: str
    sintomas: str
    contato: str

class Registro(RegistroCreate):
    id: int
    alerta: bool
    data_registro: str

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_CONTENT

@app.get("/api/registros")
async def listar_registros():
    return registros

@app.post("/api/registros")
async def criar_registro(registro: RegistroCreate):
    global registro_id_counter
    alerta = False
    
    # Regra de Negócio: Classificar como ALERTA SANITÁRIO
    # se sintomas == "Sim" OU contato == "Sim"
    if registro.sintomas == "Sim" or registro.contato == "Sim":
        alerta = True
        
    # OU se país in ["China", "Itália", "Irã"]
    if registro.pais in ["China", "Itália", "Irã"]:
        alerta = True
        
    novo_registro = Registro(
        id=registro_id_counter,
        alerta=alerta,
        data_registro=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        **registro.dict()
    )
    
    # Inserir no início da lista para exibir os mais recentes primeiro
    registros.insert(0, novo_registro)
    registro_id_counter += 1
    
    return novo_registro

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIVIG - Sistema Integrado de Vigilância Sanitária</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        sivig: '#004782',
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-50 text-gray-800 font-sans" x-data="sivigApp()">
    
    <!-- Menu Superior Fixo -->
    <nav class="bg-sivig text-white shadow-md fixed w-full z-10 top-0">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center space-x-3">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                    <span class="font-bold text-2xl tracking-wider">SIVIG</span>
                </div>
                <div class="hidden md:block">
                    <div class="flex items-baseline space-x-2">
                        <a href="#" @click.prevent="tab = 'registro'; clearSuccess();" :class="tab === 'registro' ? 'bg-blue-900 border-b-2 border-white' : 'hover:bg-blue-800'" class="px-4 py-2 rounded-t-md font-medium transition-colors">Registro de Inspeção</a>
                        <a href="#" @click.prevent="tab = 'sobre'" :class="tab === 'sobre' ? 'bg-blue-900 border-b-2 border-white' : 'hover:bg-blue-800'" class="px-4 py-2 rounded-t-md font-medium transition-colors">Sobre o SIVIG</a>
                        <a href="#" @click.prevent="tab = 'guia'" :class="tab === 'guia' ? 'bg-blue-900 border-b-2 border-white' : 'hover:bg-blue-800'" class="px-4 py-2 rounded-t-md font-medium transition-colors">Guia de Preenchimento</a>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Conteúdo Dinâmico -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-12">
        
        <!-- Tela: Registro de Inspeção -->
        <div x-show="tab === 'registro'" x-transition.opacity.duration.300ms>
            
            <!-- Mensagem de Sucesso (desaparece automaticamente) -->
            <div x-show="showSuccess" x-transition.duration.500ms class="mb-6 bg-green-100 border-l-4 border-green-500 text-green-800 p-4 rounded shadow-sm flex justify-between items-center" role="alert">
                <div class="flex items-center">
                    <svg class="h-6 w-6 text-green-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <span class="font-bold text-lg">Informações cadastradas com sucesso</span>
                </div>
                <button @click="showSuccess = false" class="text-green-700 hover:text-green-900">
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- Formulário -->
            <div class="bg-white shadow-md relative rounded-lg p-8 mb-8 border border-gray-100">
                <h2 class="text-2xl font-bold text-sivig mb-6 border-b pb-3">Triagem de Viajante</h2>
                <form @submit.prevent="submitForm">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
                        
                        <!-- Coluna 1: Dados do Viajante -->
                        <div class="space-y-5">
                            <h3 class="text-lg font-bold text-gray-800 bg-gray-50 p-2 rounded">1. Dados do Viajante</h3>
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-1">Nome Completo <span class="text-red-500">*</span></label>
                                <input type="text" x-model="form.nome" required class="block w-full rounded-md border-gray-300 shadow-sm focus:border-sivig focus:ring focus:ring-opacity-50 focus:ring-sivig px-3 py-2 border text-gray-900 bg-gray-50">
                            </div>
                            <div>
                                <label class="block text-sm font-semibold text-gray-700 mb-1">Passaporte <span class="text-red-500">*</span></label>
                                <input type="text" x-model="form.passaporte" required class="block w-full rounded-md border-gray-300 shadow-sm focus:border-sivig focus:ring focus:ring-opacity-50 focus:ring-sivig px-3 py-2 border text-gray-900 bg-gray-50 uppercase">
                            </div>
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-semibold text-gray-700 mb-1">Telefone</label>
                                    <input type="text" x-model="form.telefone" placeholder="(00) 00000-0000" x-on:input="maskPhone" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-sivig focus:ring focus:ring-opacity-50 focus:ring-sivig px-3 py-2 border text-gray-900 bg-gray-50">
                                </div>
                                <div>
                                    <label class="block text-sm font-semibold text-gray-700 mb-1">Email</label>
                                    <input type="email" x-model="form.email" placeholder="email@exemplo.com" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-sivig focus:ring focus:ring-opacity-50 focus:ring-sivig px-3 py-2 border text-gray-900 bg-gray-50">
                                </div>
                            </div>
                        </div>

                        <!-- Coluna 2: Dados de Trânsito & Triagem -->
                        <div class="space-y-5">
                            <h3 class="text-lg font-bold text-gray-800 bg-gray-50 p-2 rounded">2. Dados de Trânsito</h3>
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-semibold text-gray-700 mb-1">País de Procedência <span class="text-red-500">*</span></label>
                                    <select x-model="form.pais" required class="block w-full rounded-md border-gray-300 shadow-sm focus:border-sivig focus:ring focus:ring-opacity-50 focus:ring-sivig px-3 py-2 border text-gray-900 bg-white">
                                        <option value="" disabled selected>Selecione...</option>
                                        <option value="Brasil">Brasil</option>
                                        <option value="China">China</option>
                                        <option value="Irã">Irã</option>
                                        <option value="Itália">Itália</option>
                                        <option value="Estados Unidos">Estados Unidos</option>
                                        <option value="Espanha">Espanha</option>
                                        <option value="Outro">Outro</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-sm font-semibold text-gray-700 mb-1">Nº Voo/Embarcação</label>
                                    <input type="text" x-model="form.voo" placeholder="Ex: G3 1234" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-sivig focus:ring focus:ring-opacity-50 focus:ring-sivig px-3 py-2 border text-gray-900 bg-gray-50 uppercase">
                                </div>
                            </div>

                            <h3 class="text-lg font-bold text-gray-800 bg-gray-50 p-2 rounded mt-6">3. Triagem Epidemiológica</h3>
                            <div class="bg-red-50 p-4 rounded-md border border-red-100">
                                <div class="mb-4">
                                    <label class="block text-sm font-semibold text-gray-900 mb-2">Apresenta febre, tosse ou dificuldade respiratória? <span class="text-red-500">*</span></label>
                                    <div class="flex space-x-6">
                                        <label class="inline-flex items-center cursor-pointer">
                                            <input type="radio" x-model="form.sintomas" value="Sim" required class="w-5 h-5 text-sivig border-gray-300 focus:ring-sivig">
                                            <span class="ml-2 font-medium">Sim</span>
                                        </label>
                                        <label class="inline-flex items-center cursor-pointer">
                                            <input type="radio" x-model="form.sintomas" value="Não" required class="w-5 h-5 text-sivig border-gray-300 focus:ring-sivig">
                                            <span class="ml-2 font-medium">Não</span>
                                        </label>
                                    </div>
                                </div>
                                <div>
                                    <label class="block text-sm font-semibold text-gray-900 mb-2">Teve contato com caso suspeito/confirmado? <span class="text-red-500">*</span></label>
                                    <div class="flex space-x-6">
                                        <label class="inline-flex items-center cursor-pointer">
                                            <input type="radio" x-model="form.contato" value="Sim" required class="w-5 h-5 text-sivig border-gray-300 focus:ring-sivig">
                                            <span class="ml-2 font-medium">Sim</span>
                                        </label>
                                        <label class="inline-flex items-center cursor-pointer">
                                            <input type="radio" x-model="form.contato" value="Não" required class="w-5 h-5 text-sivig border-gray-300 focus:ring-sivig">
                                            <span class="ml-2 font-medium">Não</span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="flex justify-end border-t pt-5 mt-4 text-right">
                        <button type="submit" :disabled="loading" class="bg-sivig hover:bg-blue-800 text-white font-bold py-3 px-8 rounded shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sivig transition duration-150 ease-in-out disabled:opacity-70 flex items-center">
                            <svg x-show="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            <span x-text="loading ? 'Processando...' : 'Salvar Registro'"></span>
                        </button>
                    </div>
                </form>
            </div>

            <!-- Tabela de Registros com Atualização Dinâmica -->
            <div class="bg-white shadow-md rounded-lg overflow-hidden border border-gray-100">
                <div class="px-6 py-4 border-b bg-gray-50 flex justify-between items-center">
                    <h3 class="text-lg font-bold text-gray-800">Últimos Registros (Operação Local)</h3>
                    <span class="text-sm text-gray-500" x-text="registros.length + ' registros encontrados'"></span>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Data / Hora</th>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Identificação do Viajante</th>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Procedência</th>
                                <th class="px-6 py-3 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Resultado da Triagem</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <!-- Loop de Registros -->
                            <template x-for="reg in registros" :key="reg.id">
                                <tr :class="reg.alerta ? 'bg-yellow-100 transition-colors' : 'hover:bg-gray-50 transition-colors'">
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 font-medium" x-text="reg.data_registro"></td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm font-bold text-gray-900" x-text="reg.nome"></div>
                                        <div class="text-xs text-gray-500 mt-1" x-text="'Passaporte: ' + reg.passaporte"></div>
                                        <div class="text-xs text-gray-400" x-show="reg.telefone || reg.email" x-text="[reg.telefone, reg.email].filter(Boolean).join(' | ')"></div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                        <div class="font-semibold" x-text="reg.pais"></div>
                                        <div class="text-xs text-gray-500" x-show="reg.voo" x-text="'Voo/Emb: ' + reg.voo"></div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <!-- Alerta Sanitário -->
                                        <div x-show="reg.alerta" class="flex items-center">
                                            <span class="px-3 py-1 inline-flex text-sm leading-5 font-bold rounded-full bg-red-100 text-red-700 border border-red-300 shadow-sm animate-pulse">
                                                <svg class="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
                                                ALERTA SANITÁRIO
                                            </span>
                                        </div>
                                        <!-- Liberado -->
                                        <div x-show="!reg.alerta">
                                            <span class="px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                                Sem Risco Aparente
                                            </span>
                                        </div>
                                    </td>
                                </tr>
                            </template>
                            
                            <!-- Estado Vazio -->
                            <tr x-show="registros.length === 0">
                                <td colspan="4" class="px-6 py-12 text-center text-gray-500">
                                    <svg class="mx-auto h-12 w-12 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    <p class="mt-2 text-sm font-medium">Nenhum registro de inspeção no momento.</p>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Tela: Sobre o SIVIG -->
        <div x-show="tab === 'sobre'" style="display: none;" x-transition.opacity.duration.300ms class="bg-white shadow-md rounded-lg p-10 border border-gray-100">
            <h2 class="text-3xl font-bold text-sivig mb-6 border-b pb-4">Sobre o SIVIG</h2>
            <div class="prose max-w-none text-gray-700 space-y-6 text-lg">
                <p>O <strong>Sistema Integrado de Vigilância Sanitária (SIVIG)</strong> é uma plataforma de triagem operacional desenvolvida para atuar na linha de frente em pontos de entrada no país, como aeroportos internacionais, portos e passagens de fronteira terrestre.</p>
                
                <div class="bg-blue-50 p-6 border-l-4 border-sivig rounded-r-lg">
                    <h4 class="font-bold text-xl text-sivig mb-2">Objetivo Principal</h4>
                    <p class="text-gray-800">Identificar proativamente passageiros e viajantes que possam representar risco à saúde pública, permitindo ações imediatas de contenção, instrução e encaminhamento médico pelas autoridades sanitárias locais antes de sua plena inserção no território nacional.</p>
                </div>

                <h3 class="font-bold text-2xl text-gray-800 mt-8 mb-4">Contexto Operacional</h3>
                <p>O SIVIG foi desenhado para ser utilizado em tablets ou computadores nas estações de fiscalização. A interface adota premissas de UX/UI voltadas para operação em ambiente de alta pressão e fluxo rápido de pessoas:</p>
                <ul class="list-disc pl-6 space-y-2">
                    <li>Contraste elevado para ambientes muito iluminados.</li>
                    <li>Campos agrupados logicamente para espelhar o fluxo natural de uma entrevista.</li>
                    <li>Acionamento visual imediato (Alertas e Badges) para diminuir carga cognitiva do fiscal.</li>
                </ul>
            </div>
        </div>

        <!-- Tela: Guia de Preenchimento -->
        <div x-show="tab === 'guia'" style="display: none;" x-transition.opacity.duration.300ms class="bg-white shadow-md rounded-lg p-10 border border-gray-100">
            <h2 class="text-3xl font-bold text-sivig mb-8 border-b pb-4">Guia de Preenchimento e Triagem</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-gray-700">
                <!-- Passo 1 -->
                <div class="bg-gray-50 p-6 rounded-lg border border-gray-200 relative">
                    <div class="absolute -top-4 -left-4 flex items-center justify-center w-10 h-10 rounded-full bg-sivig text-white font-bold text-xl shadow-lg">1</div>
                    <h4 class="text-xl font-bold text-gray-800 mb-3 mt-2">Dados do Viajante</h4>
                    <p class="text-sm">Solicite sempre o Passaporte ou Documento de Identidade oficial. Preencha os dados exatamente como constam no documento. O telefone deve conter o código do país (se aplicável) ou DDD completo.</p>
                </div>

                <!-- Passo 2 -->
                <div class="bg-gray-50 p-6 rounded-lg border border-gray-200 relative">
                    <div class="absolute -top-4 -left-4 flex items-center justify-center w-10 h-10 rounded-full bg-sivig text-white font-bold text-xl shadow-lg">2</div>
                    <h4 class="text-xl font-bold text-gray-800 mb-3 mt-2">Procedência</h4>
                    <p class="text-sm">Selecione o país onde o viajante embarcou inicialmente no trajeto atual. Países com surtos ativos já listados no sistema dispararão alertas automaticamente.</p>
                </div>

                <!-- Passo 3 -->
                <div class="bg-gray-50 p-6 rounded-lg border border-gray-200 relative">
                    <div class="absolute -top-4 -left-4 flex items-center justify-center w-10 h-10 rounded-full bg-sivig text-white font-bold text-xl shadow-lg">3</div>
                    <h4 class="text-xl font-bold text-gray-800 mb-3 mt-2">Entrevista Clínica</h4>
                    <p class="text-sm">Realize as perguntas de triagem de forma direta, observando o comportamento e o estado visual do passageiro. Respostas afirmativas devem ser marcadas e requerem encaminhamento para avaliação médica em profundidade.</p>
                </div>
            </div>
            
            <div class="mt-10 p-6 bg-yellow-50 border border-yellow-200 rounded-lg flex items-start">
                <svg class="w-8 h-8 text-yellow-600 mr-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div>
                    <h4 class="font-bold text-yellow-800">ATENÇÃO: Alertas Sanitários</h4>
                    <p class="text-yellow-700 text-sm mt-1">Ao identificar um viajante com <strong>ALERTA SANITÁRIO</strong> na tabela, isole-o imediatamente conforme Protocolo 04/MS. A tabela fornecerá uma indicação visual pulsante sempre que essa condição for detectada em tempo real.</p>
                </div>
            </div>
        </div>

    </main>

    <script>
        document.addEventListener('alpine:init', () => {
            Alpine.data('sivigApp', () => ({
                tab: 'registro',
                registros: [],
                form: {
                    nome: '', passaporte: '', telefone: '', email: '',
                    pais: '', voo: '', sintomas: '', contato: ''
                },
                loading: false,
                showSuccess: false,
                successTimeout: null,
                
                init() {
                    this.fetchRegistros();
                },

                resetForm() {
                    this.form = {
                        nome: '', passaporte: '', telefone: '', email: '',
                        pais: '', voo: '', sintomas: '', contato: ''
                    };
                },

                clearSuccess() {
                    this.showSuccess = false;
                    if(this.successTimeout) clearTimeout(this.successTimeout);
                },

                maskPhone(e) {
                    let value = e.target.value.replace(/\D/g, '');
                    let length = value.length;
                    
                    if (length > 11) value = value.slice(0, 11);
                    
                    if (length > 2) {
                        value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
                    }
                    if (length > 7) {
                        value = `${value.slice(0, 10)}-${value.slice(10)}`;
                    }
                    
                    this.form.telefone = value;
                },

                async fetchRegistros() {
                    try {
                        const res = await fetch('/api/registros');
                        this.registros = await res.json();
                    } catch (e) {
                        console.error("Erro ao carregar registros:", e);
                    }
                },

                async submitForm() {
                    this.loading = true;
                    this.clearSuccess();
                    
                    try {
                        // Uppercase para facilitar visualização
                        this.form.passaporte = this.form.passaporte.toUpperCase();
                        this.form.voo = this.form.voo.toUpperCase();

                        const res = await fetch('/api/registros', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(this.form)
                        });
                        
                        if (res.ok) {
                            const novoRegistro = await res.json();
                            
                            // Adicionar ao topo da lista em tela sem reload
                            this.registros.unshift(novoRegistro);
                            
                            // Limpar formulário
                            this.resetForm();
                            
                            // Feedback Visual
                            this.showSuccess = true;
                            
                            // Scroll suave para mostrar a mensagem
                            window.scrollTo({ top: 0, behavior: 'smooth' });
                            
                            // Ocultar automaticamente
                            this.successTimeout = setTimeout(() => {
                                this.showSuccess = false;
                            }, 5000);
                        } else {
                            alert("Verifique os dados informados. Houve um erro na comunicação.");
                        }
                    } catch (e) {
                        alert("Erro crítico de rede. Tente novamente.");
                        console.error(e);
                    } finally {
                        this.loading = false;
                    }
                }
            }));
        });
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    # Inicia o servidor local para desenvolvimento e testes
    uvicorn.run(app, host="0.0.0.0", port=8000)
