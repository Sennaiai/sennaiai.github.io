"""Build a dependency-free scientific portfolio from reviewed project summaries."""
from pathlib import Path
from html import escape as e
import json

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
Q='https://github.com/Sennaiai/Quantum-Computing/tree/main/projects/'
BIO='https://github.com/Sennaiai/Computational-Biology/tree/main/projects/Genomic_Ancestry'
PROJECTS=[
dict(slug='quantum-chemistry',branch='quantum',label='Quantum chemistry',title='Electronic structure, with independent references',
     teaser='Construct molecular Hamiltonians and separate solver accuracy from basis and active-space choices.',
     tags=['PennyLane','PySCF','VQE'],outcome='H₂: |VQE − FCI| < 1.7 × 10⁻⁹ Ha across 7 bond lengths.',
     motivation='A low variational energy alone does not establish a correct molecular simulation. These studies ask how the Hamiltonian, solver, basis and active space each affect the result.',
     implementation='H₂ bond scans, an eight-qubit HCN π-active-space VQE study, and nested active-space benchmarks for NH₃, H₂CO₃ and HCO₃⁻. The notebooks expose molecular integrals, fermionic assembly, Jordan–Wigner mapping, state preparation and physical-sector checks. RHF, PBE, FCI and CASCI provide explicitly scoped references.',
     result='Across seven STO-3G H₂ bond lengths, the saved VQE energies differ from FCI by less than 1.7 × 10⁻⁹ Ha. All nine seeded HCN runs meet the recorded active-space energy target. The scaling study compares 4-, 8- and 12-qubit spaces against the same orbital-basis references.',
     limitation='These are noiseless, finite-basis calculations. Solver agreement does not remove basis or active-space error. Fixed geometries, a frozen HCN σ framework and the absence of diffuse functions for the anion limit chemical interpretation. No experimental-accuracy or hardware claim is made.',
     note='The H₂ figure includes nuclear repulsion. FCI is exact within the selected finite basis.',
     source=Q+'Quanutm%20Chemistry%20',evidence=Q+'Quanutm%20Chemistry%20/benchmarks',
     figure='h2-source-10.png',alt='H₂ total energies and signed differences from FCI across seven bond lengths, comparing RHF, PBE, FCI and VQE.',
     caption='Saved H₂ benchmark: total energies and differences from finite-basis FCI. Figure reproduced from the executed notebook.'),
dict(slug='admet',branch='quantum',label='ADMET',title='Molecular learning across a verified runtime boundary',
     teaser='Connect molecular data preparation, counterdiabatic control and QSVT to a measurement-based learning workflow.',
     tags=['Molecular encoding','Counterdiabatic control','QSVT'],outcome='1,965 labelled molecules prepared; private execution confirmed.',
     motivation='A quantum molecular-learning pipeline needs consistent data fitting, Hamiltonian construction, circuit approximation and measurement contracts before its predictive results can be interpreted.',
     implementation='I developed the reusable library underpinning this pipeline. Morgan count fingerprints feed information-screened Ising interactions and molecule-specific counterdiabatic controls. Heralded cosine/sine QSVT branches, direct-exponential references and runtime/result bindings are checked independently. Scaffold-separated classical controls and a post-measurement logistic readout complete the disclosed workflow.',
     result='The supervised preparation retains 1,965 labelled molecular identities and all 1,975 valid structures for measurement or prediction. The author confirms successful private compilation and execution through Horizon Quantum’s Triple Alpha workflow; proprietary outputs remain confidential. Public checks reproduce the disclosed offline pipeline.',
     limitation='The Hamiltonian is a dimensionless data encoding, not an electronic-structure Hamiltonian or a calibrated biological mechanism. Public quantum ADMET predictive accuracy is not established. First-order counterdiabatic control does not improve fidelity at every tested duration. Public CI does not independently reproduce the private execution.',
     note='Reusable implementation library developed by Senay Kahsay. Collaborative project credit: Kahsay et al. Private execution is author-confirmed; proprietary measurements remain confidential.',
     source=Q+'Quantum%20Molecular%20Learning%20for%20ADMET',evidence=Q+'Quantum%20Molecular%20Learning%20for%20ADMET/results',
     figure='admet-transport.svg',alt='Counterdiabatic transport benchmark comparing bare annealing, first-order control and an exact reference at several durations.',
     caption='Public four-qubit control ablation. This figure is an offline benchmark, separate from the confidential native execution.'),
dict(slug='qft',branch='quantum',label='QFT & order finding',title='Fourier arithmetic with coherent-phase checks',
     teaser='Use a shared Fourier core for reversible arithmetic and bounded Shor order-finding experiments.',
     tags=['Qiskit','PennyLane','Reversible arithmetic'],outcome='Factors 15 with gate-built arithmetic; 21 with a compiled oracle.',
     motivation='Correct basis-state probabilities can conceal incorrect controlled phases. The study tests whether Fourier arithmetic and phase estimation implement the intended coherent transformations.',
     implementation='Qiskit and PennyLane share a checked QFT convention. Independent Fourier matrices, FFT states and arithmetic references test addition, multiplication, exponentiation and clean workspace. Continued-fraction candidates are validated modularly without a blind classical order-search fallback.',
     result='Gate-built QFT modular arithmetic factors 15. A separately labelled compiled-permutation oracle factors 21. The order-6, base-5 example modulo 21 is retained as a negative control because it fails factor extraction despite finding a valid order.',
     limitation='The N=21 oracle is a small-instance compiled construction, not scalable modular arithmetic. These are ideal bounded simulations. Gate comparisons use all-to-all connectivity and do not establish hardware performance or runtime advantage.',
     note='Arithmetic correctness, valid order finding and successful factor extraction are distinct outcomes.',
     source=Q+'QFT',evidence=Q+'QFT/results',figure='qft-order-finding.svg',
     alt='Saved Shor order-finding benchmark outcomes and logical resources for bounded instances.',
     caption='Measured order-finding evidence from the QFT study, with the compiled-oracle boundary retained.'),
dict(slug='qubo',branch='quantum',label='QUBO & QAOA',title='Airline recovery under shared capacity constraints',
     teaser='Measure allocation, audit feasibility and compare local QAOA sampling with classical annealing.',
     tags=['QUBO / Ising','Simulated annealing','QAOA'],outcome='Mean allocation: 72.19% of bookings; 61.29% of passengers.',
     motivation='Recover disrupted bookings while respecting shared seat inventory and an explicit service-cost objective. A quantum extension is evaluated against the same local QUBOs, rather than credited with the classical pipeline’s allocation rate.',
     implementation='A whole-booking capacity-slack QUBO, classical simulated annealing, route expansion and audited local improvement act on 7,653 PNRs (booking groups) and 11,822 passengers. QAOA compares structurally selected neighborhoods, one-choice mixers, exact local references and globally checked patch admission.',
     result='The expanded classical hybrid reallocates 72.19% of PNRs and 61.29% of passengers, averaged across five seeds. In the larger local study, depth-4 QAOA samples the exact S3 optimum in 13 of 18 runs, versus annealing’s 14. QAOA adds zero bookings or passengers; exact enumeration confirms local allocation saturation.',
     limitation='Local QAOA results are not full-population reallocation rates. Independent patches cannot be summed. Each exact local Pareto frontier has one nondominated point. No quantum advantage is established; the airline’s Gurobi comparison remains external.',
     note='PNR/passenger allocation and valid-sample counts have different denominators and are reported separately.',
     source=Q+'QUBO%20IROPS%20solver',evidence=Q+'QUBO%20IROPS%20solver/qaoa/expanded/results',
     figure='qaoa-comparison.svg',alt='QAOA and annealing optimum-discovery counts, alongside exact local booking-allocation ceilings.',
     caption='Larger-neighborhood QAOA study. The equal incumbent and exact-maximum bars establish the local allocation limit.'),
dict(slug='grid-load',branch='quantum',label='Electricity-grid forecasting',title='Quantum reservoirs against strong classical controls',
     teaser='Benchmark continuous-variable and analogue-spin dynamics with chronological evaluation and resource accounting.',
     tags=['Continuous variables','Spin reservoirs','Time-series ML'],outcome='324.3 MW RMSE: gradient boosting; ≈351.0 MW: quantum hybrids.',
     motivation='Test whether verified quantum reservoir features add forecasting value once data timing, model selection and classical feature access are controlled.',
     implementation='Two bosonic modes use Gaussian/Kerr ablations and Fock-cutoff checks; six interacting spins use exact dynamics and independent Qiskit references. Expanding validation folds select models before a fixed test interval. Persistence, seasonal forecasts, ridge, random forest, gradient boosting and a classical reservoir provide matched controls.',
     result='Across 2,823 held-out targets, gradient boosting reaches 324.3 MW RMSE. Both Kerr-hybrid and interacting-spin-hybrid ensembles reach approximately 351.0 MW; persistence reaches 806.4 MW. Verified quantum dynamics and resource estimates are retained alongside this negative predictive-advantage result.',
     limitation='This is a historical 30-minute-ahead hindcast, not an operational forecast. One geographic series and seasonal holdout do not establish general superiority. Routing, calibration and hardware noise are not modelled; seed spread and temporal uncertainty do not guarantee absence of overfitting.',
     note='Based on the QUAC 605 collaborative project; full contributor credits are retained in the repository.',
     source=Q+'Grid%20Load%20QRC%20Benchmarks',evidence=Q+'Grid%20Load%20QRC%20Benchmarks/results',
     figure='grid-spin.svg',alt='Analogue-spin reservoir forecasting results compared with classical baselines and resource diagnostics.',
     caption='Saved benchmark. Demand data: National Energy SO, NESO Open Licence. Original collaboration is credited in the project guide.'),
dict(slug='bioinformatics',branch='biology',label='Bioinformatics',title='A modular genomic-ancestry workflow',
     teaser='Connect contamination estimates, principal components and reference-population assignment in Snakemake.',
     tags=['Snakemake','VerifyBamID2','PCA / KNN'],outcome='A modular workflow for genomic quality control and population assignment.',
     motivation='Make ancestry-related quality control and population assignment inspectable as one modular workflow, with explicit reference resources and sample alignment.',
     implementation='The workflow connects GRCh38 preparation and VerifyBamID2 outputs to contamination tables, harmonized principal components, a four-PC K-nearest-neighbor classifier and PCA visualizations. Python tests cover table alignment, PC-column parsing and a small synthetic assignment case.',
     result='The repository implements the processing stages and synthetic reference tests. Its outputs are contamination summaries, aligned PC tables, population-label tables and plots. No cohort-level accuracy or benchmark measurements are published here.',
     limitation='Reference genomes, compatible 1000 Genomes resources and authorized sample inputs are required for a full run. Existing synthetic tests do not validate end-to-end cohort behavior, biological generalization or clinical suitability. No individual genomic records are displayed.',
     note='Software implementation evidence is distinct from a validated ancestry-inference result.',
     source=BIO,evidence='https://github.com/Sennaiai/Computational-Biology/tree/main/tests',figure=None,alt='',caption=''),
]

def header(prefix=''):
    return f'''<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="shell header-inner"><a class="brand" href="{prefix}index.html">Senay Kahsay<span>Scientific portfolio</span></a><nav aria-label="Primary"><a href="{prefix}index.html#work">Work</a><a href="{prefix}index.html#about">About</a><a href="{prefix}index.html#contact">Contact</a></nav></div></header>'''

def footer(prefix=''):
    return '''<footer class="site-footer"><div class="shell footer-inner"><p>Senay Kahsay <span>Quantum computing · Life Sciences</span></p><p><a href="https://github.com/Sennaiai">GitHub</a><a href="https://www.linkedin.com/in/senay-kahsay">LinkedIn</a></p><small>© 2026 Senay Kahsay. Source methods, credits and limitations accompany each study.</small></div></footer>'''

def page(title,description,body,prefix=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(description)}"><meta name="robots" content="index,follow"><meta name="color-scheme" content="light"><title>{e(title)} · Senay Kahsay</title><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css"></head><body>{header(prefix)}{body}{footer(prefix)}</body></html>'''

def card(p,feature=False):
    return f'''<article class="project-card {'feature' if feature else ''} {p['branch']}"><div class="card-top"><span class="eyebrow">{e(p['label'])}</span><span class="project-type">{'Quantum computing' if p['branch']=='quantum' else 'Life Sciences'}</span></div><h3><a href="projects/{p['slug']}.html">{e(p['title'])}</a></h3><p>{e(p['teaser'])}</p><p class="outcome">{e(p['outcome'])}</p><div class="card-bottom"><ul class="tags" aria-label="Methods">{''.join('<li>'+e(t)+'</li>' for t in p['tags'])}</ul><a class="text-link" href="projects/{p['slug']}.html">Read study<span class="sr-only">: {e(p['label'])}</span></a></div></article>'''

home='''<main id="main"><section class="hero shell"><div class="hero-copy"><p class="eyebrow">Computational research · Scientific software</p><h1>Quantum computing<br>and Life Sciences</h1><p class="hero-lede">Scientific software and tools for molecular studies, with explicit models, independent checks, reproducible implementations and CI-tested code.</p><p class="hero-tools">Frontier AI development and productivity tools.</p><p class="qualification">Master of Quantum Computing graduate from the University of Calgary, with a background in molecular biology (Honors) and philosophy.</p><div class="hero-links"><a class="button primary" href="#quantum">Quantum computing</a><a class="button secondary" href="#biology">Life Sciences</a></div></div><figure class="hero-figure"><img src="assets/research-sketch.svg" alt="HCN molecular-model sketch and saved H₂ total FCI energies in the STO-3G basis, at four bond lengths." width="480" height="400"><figcaption>Algorithm development: clear specifications, modular code, reference tests and continuous integration.</figcaption></figure></section>
<section class="work-section shell" id="work"><div class="section-heading" id="quantum"><div><p class="eyebrow">Quantum computing</p><h2>From molecular models<br>to measured comparisons.</h2></div></div><div class="project-grid">'''+''.join(card(p,i==0) for i,p in enumerate(PROJECTS) if p['branch']=='quantum')+'''</div></section>
<section class="biology-section" id="biology"><div class="shell"><div class="section-heading"><div><p class="eyebrow">Life Sciences</p><h2>Biological problems.</h2></div></div><div class="project-grid biology-grid">'''+card(PROJECTS[-1])+'''<aside class="workflow-panel"><p class="eyebrow">Genomic data workflow</p><ol><li>Contamination and ancestry PCs<span>VerifyBamID2 outputs</span></li><li>Reference alignment<span>Sample IDs and four principal components</span></li><li>Population assignment<span>KNN classification and visual summaries</span></li></ol><p>Implementation evidence is presented separately from unreported cohort performance.</p></aside></div></div></section>
<section class="about-section shell" id="about"><div><p class="eyebrow">About</p><h2>Bridging quantum computing<br>and life sciences.</h2></div><div class="about-copy"><p>I bridge quantum computing and the life sciences, with interests in quantum chemistry, molecular learning and computational approaches to biological systems. I investigate where quantum computing can offer an advantage over classical methods.</p></div></section>
<section class="contact-section" id="contact"><div class="shell contact-inner"><div><p class="eyebrow">Contact</p><h2>Let’s connect.</h2><p>For research and scientific-software conversations, connect through LinkedIn or explore the linked implementations.</p></div><div class="contact-links"><a class="button primary" href="https://www.linkedin.com/in/senay-kahsay">Connect on LinkedIn</a><a class="text-link" href="https://github.com/Sennaiai">GitHub profile</a></div></div></section></main>'''
DIST.mkdir(exist_ok=True);(DIST/'projects').mkdir(exist_ok=True)
(DIST/'index.html').write_text(page('Scientific portfolio','Senay Kahsay: quantum computing and life sciences. Scientific software, molecular learning and computational biology.',home))
for p in PROJECTS:
    figure=f'''<figure class="evidence-figure"><img src="../assets/{p['figure']}" alt="{e(p['alt'])}" loading="lazy"><figcaption>{e(p['caption'])}</figcaption></figure>''' if p['figure'] else ''
    sections=''.join(f'<section class="study-block"><h2>{label}</h2><p>{e(p[key])}</p></section>' for key,label in [('motivation','Motivation'),('implementation','Implementation'),('result','Results'),('limitation','Limitations')])
    body=f'''<main id="main" class="study-main"><section class="study-hero shell"><a class="breadcrumb" href="../index.html#{'quantum' if p['branch']=='quantum' else 'biology'}">{'Quantum computing' if p['branch']=='quantum' else 'Life Sciences'}</a><p class="eyebrow">{e(p['label'])}</p><h1>{e(p['title'])}</h1><p class="study-lede">{e(p['teaser'])}</p><ul class="tags" aria-label="Methods">{''.join('<li>'+e(t)+'</li>' for t in p['tags'])}</ul></section><div class="shell"><div class="study-outcome"><span class="eyebrow">Main outcome</span><p>{e(p['outcome'])}</p></div><div class="study-grid">{sections}</div>{figure}<aside class="study-note"><strong>Evidence boundary</strong><p>{e(p['note'])}</p></aside><div class="source-links"><a class="button primary" href="{p['source']}">Project guide and source</a><a class="button secondary" href="{p['evidence']}">Evidence and checks</a><a class="text-link" href="../index.html#work">All selected work</a></div></div></main>'''
    (DIST/'projects'/f"{p['slug']}.html").write_text(page(p['label'],p['teaser'],body,'../'))
(ROOT/'content').mkdir(exist_ok=True)
(ROOT/'content/projects.json').write_text(json.dumps(PROJECTS,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'pages':7,'projects':len(PROJECTS),'branches':['quantum','biology']}))
