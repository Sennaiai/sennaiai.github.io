"""Content, navigation and privacy contracts for the static portfolio."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re,unittest,statistics

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'


class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.images=[];self.headings=[];self.current=None;self.title='';self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        if tag in ('a','link') and a.get('href'):self.links.append(a['href'])
        if tag=='img':self.images.append(a)
        if tag in ('h1','h2','title'):self.current=tag;self.headings.append([tag,''])
    def handle_data(self,data):
        if self.current:self.headings[-1][1]+=data
    def handle_endtag(self,tag):
        if tag==self.current:self.current=None


class PortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages={p:Page(p.read_text()) for p in DIST.rglob('*.html')}
        cls.projects=json.loads((ROOT/'content/projects.json').read_text())

    def test_three_branches_preserve_existing_projects_and_selected_additions(self):
        self.assertEqual(len(self.projects),10)
        self.assertEqual(sum(p['branch']=='quantum' for p in self.projects),5)
        self.assertEqual(sum(p['branch']=='biology' for p in self.projects),1)
        self.assertEqual(sum(p['branch']=='classical' for p in self.projects),4)
        self.assertEqual({p['slug'] for p in self.projects},{'quantum-chemistry','admet','qft','qubo','grid-load','bioinformatics','classical-learning','monte-carlo','multiobjective-optimization','fuzzy-allocation'})
        mini=[p['slug'] for p in self.projects if p.get('display')=='mini']
        self.assertEqual(mini,['fuzzy-allocation'])

    def test_learning_reuse_and_third_branch_are_discoverable(self):
        home=(DIST/'index.html').read_text()
        self.assertIn('id="classical"',home)
        self.assertIn('href="#classical"',home)
        self.assertEqual(home.count('class="mini-study"'),1)
        learning=(DIST/'projects/classical-learning.html').read_text()
        for phrase in ('Ridge','random forest','gradient boosting','echo-state','logistic','ADMET','portable'):
            self.assertIn(phrase,learning)
        for related in ('admet.html','grid-load.html'):
            self.assertIn(f'href="{related}"',learning)
        for p in self.projects:
            if p['branch']=='classical':
                self.assertIn('href="../index.html#classical"',(DIST/'projects'/f"{p['slug']}.html").read_text())
                self.assertLess(sum(len(p[k].split()) for k in ('motivation','implementation','result','limitation')),180)
                self.assertNotRegex(p['outcome'],r'(?i)tests? pass|passing tests?|checks? pass')

    def test_new_metrics_match_extracted_numerical_records(self):
        evidence=ROOT/'content/evidence'
        mc=json.loads((evidence/'monte-carlo.json').read_text())['records']
        projects={p['slug']:p for p in self.projects}
        for method in ('mc','scrambled_sobol'):
            rows=[v for v in mc if v['method']==method]
            self.assertEqual({v['seed'] for v in rows},{7,19,41,73})
            self.assertTrue(all(v['total_payoff_evaluations']==131072 for v in rows))
            rmse=statistics.mean(v['absolute_error']**2 for v in rows)**.5
            self.assertIn(f'{rmse:.3g}',projects['monte-carlo']['outcome'])
        unit=json.loads((evidence/'multiobjective.json').read_text())['records']
        for method in ('mopso','qpso'):
            rows=[v for v in unit if v['method']==method]
            self.assertEqual(len(rows),5)
            self.assertTrue(all(v['candidate_evaluations']==4530 and v['all_schedules_feasible'] for v in rows))
            self.assertIn(f"{statistics.median(v['normalized_hypervolume'] for v in rows):.4f}",projects['multiobjective-optimization']['outcome'])
        learning=json.loads((evidence/'classical-learning.json').read_text())
        self.assertEqual(learning['test_targets'],2823)
        self.assertIn(f"{learning['models']['gradient_boosting']['RMSE_MW']:.1f}",projects['classical-learning']['result'])
        self.assertIn('no ADMET predictive accuracy',projects['classical-learning']['result'])

    def test_every_internal_link_asset_and_fragment_resolves(self):
        for path,page in self.pages.items():
            for href in page.links+[im['src'] for im in page.images]:
                url=urlsplit(href)
                if url.scheme or url.netloc:continue
                target=(path.parent/unquote(url.path)).resolve() if url.path else path
                self.assertTrue(target.is_relative_to(DIST),href)
                self.assertTrue(target.is_file(),(path,href))
                if url.fragment and target.suffix=='.html':self.assertIn(url.fragment,self.pages[target].ids)

    def test_each_case_has_complete_scientific_structure(self):
        for project in self.projects:
            page=self.pages[DIST/'projects'/f"{project['slug']}.html"]
            headings=[text for tag,text in page.headings if tag=='h2']
            for name in ('Motivation','Implementation','Results','Limitations'):self.assertIn(name,headings)

    def test_accessibility_basics_are_present(self):
        for path,page in self.pages.items():
            text=path.read_text()
            self.assertEqual(sum(tag=='h1' for tag,t in page.headings),1,path)
            self.assertTrue(any(tag=='title' and t.strip() for tag,t in page.headings))
            self.assertIn('lang="en"',text);self.assertIn('name="viewport"',text)
            self.assertIn('Skip to content',text)
            self.assertTrue(all(im.get('alt','').strip() for im in page.images))

    def test_sensitive_or_unfounded_claims_are_absent(self):
        text='\n'.join(p.read_text() for p in DIST.rglob('*.html'))
        for forbidden in ('HGDP00082','HGDP00450','/Users/','/private/tmp/','TRIPLE_ALPHA_API_KEY','sk-proj-','candidate @','coming soon','TODO','codex-preview'):
            self.assertNotIn(forbidden,text)
        self.assertIn('author-confirmed',text.lower())
        self.assertIn('No cohort-level accuracy',text)
        self.assertIn('not an electronic-structure Hamiltonian',text)
        self.assertIn('not full-population reallocation rates',text)

    def test_requested_copy_and_github_sources(self):
        home=(DIST/'index.html').read_text()
        for phrase in ('Quantum computing<br>and Life Sciences','Biological problems.','Let’s connect.','Frontier AI development and productivity tools.','CI-tested code','Master of Quantum Computing graduate'):
            self.assertIn(phrase,home)
        for removed in ('Five themes, with','Bioinformatics is the current focus','Discuss the science.','Each study makes its evidence boundary explicit'):
            self.assertNotIn(removed,home)
        self.assertNotIn('I use frontier AI tools',home)
        self.assertNotIn('medium.com',home)
        self.assertNotIn('9 passing synthetic tests',home)
        biology=next(p for p in self.projects if p['slug']=='bioinformatics')
        self.assertNotRegex(biology['outcome'],r'\d|accuracy|F1|AUC')
        self.assertIn('324.3 MW RMSE',home)
        self.assertIn('≈351.0 MW',home)
        for metric in ('1.7 × 10⁻⁹ Ha','7 bond lengths','1,965 labelled molecules prepared','15 with gate-built arithmetic; 21 with a compiled oracle','61.29% of passengers'):
            self.assertIn(metric,home)
        for project in self.projects:
            for key in ('source','evidence'):
                self.assertEqual(urlsplit(project[key]).hostname,'github.com')
        admet=(DIST/'projects/admet.html').read_text()
        self.assertIn('I developed the ADMET application and, in collaboration with colleagues, the reusable Triple Alpha/Beryllium simulation library.',admet)
        self.assertIn('ADMET application developed by Senay Kahsay; reusable simulation library co-developed with colleagues.',admet)
        svg=(DIST/'assets/research-sketch.svg').read_text()
        self.assertNotIn('GENOMIC DATA',svg)
        for r in json.loads((ROOT/'content/evidence/h2.json').read_text())['scan']:
            if r['distance_angstrom'] in (.5,.74,1.5,3.):
                self.assertIn(f"{r['fci_hartree']:.6f}",svg)

    def test_requested_layout_and_collaboration_contracts(self):
        home=(DIST/'index.html').read_text()
        self.assertLess(home.index('class="hero shell"'),home.index('id="about"'))
        self.assertLess(home.index('id="about"'),home.index('id="work"'))
        self.assertLess(home.index('id="work"'),home.index('id="contact"'))
        figure=re.search(r'<figure class="hero-figure">(.*?)</figure>',home,re.S).group(1)
        self.assertLess(figure.index('Algorithm development:'),figure.index('Frontier AI development'))
        self.assertEqual(home.count('Frontier AI development and productivity tools.'),1)
        self.assertIn('At Horizon Quantum, I worked on a quantum pipeline for modeling drug properties and tested its circuits against exact numerical calculations.',home)
        for slug in ('admet','grid-load'):
            text=(DIST/'projects'/f'{slug}.html').read_text()
            self.assertIn('<strong>Collaboration</strong>',text)
            self.assertIn('Full contribution credits are retained in the repository.',text)
            self.assertNotIn('<strong>Evidence boundary</strong>',text)
        for slug in ('bioinformatics','classical-learning'):
            self.assertNotIn('class="study-note"',(DIST/'projects'/f'{slug}.html').read_text())
        bio=(DIST/'projects/bioinformatics.html').read_text()
        self.assertNotIn('Existing synthetic tests do not validate',bio)
        self.assertNotRegex((DIST/'projects/qubo.html').read_text(),r'\bS3\b')
        for p in self.projects:
            self.assertRegex(p['teaser'],r'^(Constructed|Developed|Implemented|Measured|Benchmarked|Connected|Compared|Evaluated)\b')

    def test_public_source_is_small_and_has_no_hosting_metadata(self):
        self.assertFalse((ROOT/'.openai').exists())
        for path in (ROOT/'content/evidence').glob('*.json'):
            self.assertLess(path.stat().st_size,100_000)
        for path in DIST.rglob('*'):
            if path.suffix in ('.html','.svg','.css'):
                self.assertNotIn('chatgpt',path.read_text().lower())

    def test_key_results_match_repository_evidence(self):
        q=ROOT/'content/evidence'
        for item in json.loads((q/'manifest.json').read_text()):
            self.assertEqual(hashlib.sha256((q/item['file']).read_bytes()).hexdigest(),item['sha256'])
        h=json.loads((q/'h2.json').read_text())
        self.assertLess(max(abs(r['vqe_hartree']-r['fci_hartree']) for r in h['scan']),1.7e-9)
        c=json.loads((q/'hcn.json').read_text())
        self.assertEqual(sum(len(r['runs']) for r in c['scan']),9)
        self.assertTrue(all(v['accuracy_target_met'] for r in c['scan'] for v in r['runs']))
        r=json.loads((q/'qaoa.json').read_text())
        s={v['method']:v for v in r['summary']}
        self.assertEqual((s['onechoice_QAOA_p4']['local_S3_optimum_runs'],s['neal']['local_S3_optimum_runs']),(13,14))
        self.assertTrue(all(v['max_added_PNRs_in_one_patch']==0 for v in r['summary']))


if __name__=='__main__':unittest.main()
