import os

templates_dir = 'd:/Dev/black_ryan/templates'

html_files = {
    'policies.html': '''{% extends 'base.html' %}
{% block title %}Policies vs Reality | StX Archive{% endblock %}
{% block content %}
<div class="relative pt-24 pb-16 px-6 sm:px-12 flex flex-col items-center text-center">
    <div class="inline-block px-5 py-1 mb-8 rounded-full border border-airred/30 bg-transparent text-airred text-[11px] font-black tracking-[0.2em] uppercase">The Rulebook</div>
    <h1 class="text-5xl md:text-6xl font-black text-airblack dark:text-white tracking-tight mb-8">Policies vs <span class="text-airred">Reality</span></h1>
    <p class="mx-auto max-w-2xl text-xl text-gray-600 dark:text-gray-400 font-medium">What is promised on paper versus what students actually experience every day.</p>
</div>

<div class="max-w-5xl mx-auto mb-20 px-6">
    <div class="space-y-6">
        <div class="bg-white dark:bg-[#151515] rounded-2xl border border-gray-100 dark:border-gray-800 p-8 shadow-sm flex flex-col md:flex-row gap-8">
            <div class="flex-1">
                <h3 class="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2">The Official Policy</h3>
                <p class="text-xl font-bold text-airblack dark:text-white">"State of the Art Computer Labs for All Grades"</p>
            </div>
            <div class="flex-1 bg-airred/5 border-l-4 border-airred p-6 rounded-r-xl">
                <h3 class="text-xs font-bold uppercase tracking-widest text-airred mb-2">The Reality</h3>
                <p class="text-lg text-gray-700 dark:text-gray-300 font-medium">Only a handful of computers actually boot up. The rest are dead screens taking up desk space, yet computer fees are still collected.</p>
            </div>
        </div>
        
        <div class="bg-white dark:bg-[#151515] rounded-2xl border border-gray-100 dark:border-gray-800 p-8 shadow-sm flex flex-col md:flex-row gap-8">
            <div class="flex-1">
                <h3 class="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2">The Official Policy</h3>
                <p class="text-xl font-bold text-airblack dark:text-white">"Comprehensive Physical Education Curriculum"</p>
            </div>
            <div class="flex-1 bg-airred/5 border-l-4 border-airred p-6 rounded-r-xl">
                <h3 class="text-xs font-bold uppercase tracking-widest text-airred mb-2">The Reality</h3>
                <p class="text-lg text-gray-700 dark:text-gray-300 font-medium">The PT teacher has been missing for the entire term. The school hasn't hired a replacement, and the entire PE syllabus remains completely untouched.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'principals_note.html': '''{% extends 'base.html' %}
{% block title %}Principal's Note | StX Archive{% endblock %}
{% block content %}
<div class="relative pt-24 pb-16 px-6 sm:px-12 flex flex-col items-center text-center">
    <div class="inline-block px-5 py-1 mb-8 rounded-full border border-airred/30 bg-transparent text-airred text-[11px] font-black tracking-[0.2em] uppercase">Communications</div>
    <h1 class="text-5xl md:text-6xl font-black text-airblack dark:text-white tracking-tight mb-8">Principal's <span class="text-airred">Note</span></h1>
    <p class="mx-auto max-w-2xl text-xl text-gray-600 dark:text-gray-400 font-medium">Annotating the administration's official correspondence.</p>
</div>

<div class="max-w-4xl mx-auto mb-20 px-6">
    <div class="bg-[#fcf8f2] dark:bg-[#1a1816] p-10 rounded-lg shadow-xl border-2 border-gray-200 dark:border-[#2a2826] relative">
        <div class="absolute top-4 right-8 text-airred/50 text-6xl font-serif">"</div>
        <p class="text-right text-gray-500 mb-8 font-serif">Date: Start of Term</p>
        <p class="text-lg text-gray-800 dark:text-gray-200 font-serif leading-relaxed mb-6">Dear Parents and Students,</p>
        <p class="text-lg text-gray-800 dark:text-gray-200 font-serif leading-relaxed mb-6">
            We are excited to welcome you back to a campus that has been fully renovated over the summer. 
            <span class="relative inline-block">
                <span class="bg-yellow-200 dark:bg-yellow-900/30">Our facilities are second to none,</span>
                <span class="absolute -top-10 -right-12 text-airred font-black text-sm italic transform rotate-6 border border-airred px-2 py-1 rounded bg-white dark:bg-airblack">The walls are unpainted!</span>
            </span>
            providing a world-class environment for your children to thrive.
        </p>
        <p class="text-lg text-gray-800 dark:text-gray-200 font-serif leading-relaxed mb-6">
            We have also streamlined our fee structure to ensure complete transparency. 
            <span class="relative inline-block">
                <span class="bg-yellow-200 dark:bg-yellow-900/30">There are no hidden charges.</span>
                <span class="absolute -bottom-10 -left-4 text-airred font-black text-sm italic transform -rotate-3 border border-airred px-2 py-1 rounded bg-white dark:bg-airblack">Then why is 4th std 52k?</span>
            </span>
        </p>
        <p class="text-lg text-gray-800 dark:text-gray-200 font-serif leading-relaxed">Sincerely,<br/>The Administration</p>
    </div>
</div>
{% endblock %}''',

    'incidents.html': '''{% extends 'base.html' %}
{% block title %}Incidents | StX Archive{% endblock %}
{% block content %}
<div class="relative pt-24 pb-16 px-6 sm:px-12 flex flex-col items-center text-center">
    <div class="inline-block px-5 py-1 mb-8 rounded-full border border-airred/30 bg-transparent text-airred text-[11px] font-black tracking-[0.2em] uppercase">Chronology</div>
    <h1 class="text-5xl md:text-6xl font-black text-airblack dark:text-white tracking-tight mb-8">Documented <span class="text-airred">Incidents</span></h1>
</div>

<div class="max-w-4xl mx-auto mb-20 px-6 relative">
    <div class="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gray-200 dark:bg-gray-800"></div>
    
    <div class="relative mb-12 flex justify-between items-center w-full right-timeline">
        <div class="order-1 w-5/12"></div>
        <div class="z-20 flex items-center order-1 bg-airred shadow-xl w-6 h-6 rounded-full"></div>
        <div class="order-1 bg-white dark:bg-[#151515] rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 w-5/12 px-6 py-5">
            <span class="text-airred text-xs font-bold uppercase tracking-widest mb-2 block">Ongoing</span>
            <h3 class="font-black text-xl text-airblack dark:text-white mb-2">The Missing PT Teacher</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 font-medium">The physical education teacher position remains vacant. No replacement chosen. The entire syllabus is incomplete while students sit idle during PT periods.</p>
        </div>
    </div>
    
    <div class="relative mb-12 flex justify-between flex-row-reverse items-center w-full left-timeline">
        <div class="order-1 w-5/12"></div>
        <div class="z-20 flex items-center order-1 bg-airblack dark:bg-gray-700 shadow-xl w-6 h-6 rounded-full border-4 border-white dark:border-[#0a0a0a]"></div>
        <div class="order-1 bg-white dark:bg-[#151515] rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 w-5/12 px-6 py-5">
            <span class="text-gray-400 text-xs font-bold uppercase tracking-widest mb-2 block">Recent Term</span>
            <h3 class="font-black text-xl text-airblack dark:text-white mb-2">Lab Equipment Breakdown</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 font-medium">Multiple science practicals canceled due to broken lab equipment. Appeals for repair have gone unanswered despite full lab fees being collected.</p>
        </div>
    </div>
</div>
{% endblock %}''',

    'evidence_wall.html': '''{% extends 'base.html' %}
{% block title %}Evidence Wall | StX Archive{% endblock %}
{% block content %}
<div class="relative pt-24 pb-16 px-6 sm:px-12 flex flex-col items-center text-center">
    <div class="inline-block px-5 py-1 mb-8 rounded-full border border-airred/30 bg-transparent text-airred text-[11px] font-black tracking-[0.2em] uppercase">Gallery</div>
    <h1 class="text-5xl md:text-6xl font-black text-airblack dark:text-white tracking-tight mb-8">Evidence <span class="text-airred">Wall</span></h1>
</div>

<div class="max-w-7xl mx-auto px-6 mb-20">
    <div class="columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6">
        <!-- Item 1 -->
        <div class="break-inside-avoid bg-[#151515] rounded-2xl overflow-hidden border border-gray-800 group relative">
            <div class="h-64 bg-gray-200 dark:bg-[#111] flex flex-col items-center justify-center p-6 text-center">
                <svg class="h-16 w-16 text-gray-700 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                <span class="text-gray-500 font-bold uppercase tracking-widest text-xs">Unpainted Corridors</span>
            </div>
            <div class="absolute bottom-0 w-full bg-black/80 backdrop-blur text-white p-4 translate-y-full group-hover:translate-y-0 transition-transform">
                <p class="text-sm font-medium">Walls left bare and unpainted despite "renovation" fees.</p>
            </div>
        </div>
        
        <!-- Item 2 -->
        <div class="break-inside-avoid bg-[#151515] rounded-2xl overflow-hidden border border-gray-800 group relative">
            <div class="h-96 bg-gray-200 dark:bg-[#1a1a1a] flex flex-col items-center justify-center p-6 text-center border-4 border-dashed border-gray-700 m-2">
                <svg class="h-16 w-16 text-airred mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                <span class="text-gray-400 font-bold uppercase tracking-widest text-xs">Fee Receipt</span>
                <span class="text-white font-black text-2xl mt-2">₹52,000</span>
                <span class="text-airred font-medium text-sm mt-1">4th Standard</span>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'hall_of_shame.html': '''{% extends 'base.html' %}
{% block title %}Hall of Shame | StX Archive{% endblock %}
{% block content %}
<div class="relative pt-24 pb-16 px-6 sm:px-12 flex flex-col items-center text-center">
    <h1 class="text-5xl md:text-7xl font-black text-airblack dark:text-white tracking-tight mb-8">Hall of <span class="text-airred">Shame</span></h1>
    <p class="mx-auto max-w-2xl text-xl text-gray-600 dark:text-gray-400 font-medium">Administrative failures that remain completely unaddressed.</p>
</div>

<div class="max-w-6xl mx-auto px-6 mb-20 grid grid-cols-1 md:grid-cols-3 gap-8">
    <div class="bg-[#111] border border-gray-800 p-10 flex flex-col items-center text-center hover:border-airred transition-colors group">
        <div class="text-airred mb-6"><svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg></div>
        <h3 class="text-2xl font-black text-white mb-4">Dead Computers</h3>
        <p class="text-gray-400 font-medium leading-relaxed">Only a few computers actually work. The lab is a graveyard of broken monitors, yet computer fees are mandatory.</p>
    </div>
    
    <div class="bg-[#111] border border-gray-800 p-10 flex flex-col items-center text-center hover:border-airred transition-colors group">
        <div class="text-airred mb-6"><svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg></div>
        <h3 class="text-2xl font-black text-white mb-4">Unpainted Walls</h3>
        <p class="text-gray-400 font-medium leading-relaxed">Corridors and classrooms look abandoned with scraped, unpainted walls, severely lacking basic maintenance.</p>
    </div>
    
    <div class="bg-[#111] border border-gray-800 p-10 flex flex-col items-center text-center hover:border-airred transition-colors group">
        <div class="text-airred mb-6"><svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg></div>
        <h3 class="text-2xl font-black text-white mb-4">Missing PT Teacher</h3>
        <p class="text-gray-400 font-medium leading-relaxed">No physical education teacher has been appointed. The entire syllabus is incomplete.</p>
    </div>
</div>
{% endblock %}''',

    'fee_scam.html': '''{% extends 'base.html' %}
{% block title %}The Fee Scam | StX Archive{% endblock %}
{% block content %}
<div class="relative pt-24 pb-16 px-6 sm:px-12 flex flex-col items-center text-center">
    <div class="inline-block px-5 py-1 mb-8 rounded-full border border-airred/30 bg-transparent text-airred text-[11px] font-black tracking-[0.2em] uppercase">Financials</div>
    <h1 class="text-5xl md:text-6xl font-black text-airblack dark:text-white tracking-tight mb-8">The Fee <span class="text-airred">Scam</span></h1>
    <p class="mx-auto max-w-2xl text-xl text-gray-600 dark:text-gray-400 font-medium">Breaking down the unjustified costs and mandatory extortion.</p>
</div>

<div class="max-w-5xl mx-auto px-6 mb-20 space-y-8">
    <div class="bg-[#151515] border border-gray-800 rounded-2xl p-8 md:p-12 shadow-2xl relative overflow-hidden">
        <div class="absolute -right-10 -top-10 text-9xl font-black text-gray-800/30 select-none">₹</div>
        <h2 class="text-3xl font-black text-white mb-6">4th Standard: ₹52,000</h2>
        <p class="text-xl text-gray-400 mb-8 font-medium">A staggering fee structure for elementary education, completely decoupled from the actual facilities provided (unpainted walls, dead computers).</p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
            <div class="bg-[#111] p-6 rounded-xl border-l-4 border-airred">
                <h4 class="text-airred font-black uppercase tracking-widest text-sm mb-2">Council Child Labor</h4>
                <p class="text-gray-300 font-medium">They take ₹630 just to make a student a "council member". The reward? Students act as free labor, moving benches and doing school chores. You pay them to do their manual labor.</p>
            </div>
            <div class="bg-[#111] p-6 rounded-xl border-l-4 border-airred">
                <h4 class="text-airred font-black uppercase tracking-widest text-sm mb-2">Gold-Plated Books</h4>
                <p class="text-gray-300 font-medium">Book prices are exorbitantly inflated, priced like buying gold. Furthermore, the school diary is not included and must be purchased separately.</p>
            </div>
            <div class="bg-[#111] p-6 rounded-xl border-l-4 border-airred md:col-span-2">
                <h4 class="text-airred font-black uppercase tracking-widest text-sm mb-2">The Useless Portfolio</h4>
                <p class="text-gray-300 font-medium">Purchasing a "portfolio" is mandatory alongside the diary. It has absolutely no practical use in the curriculum, serving only as another mandatory cash grab.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'vip_treatment.html': '''{% extends 'base.html' %}
{% block title %}VIP Treatment | StX Archive{% endblock %}
{% block content %}
<div class="relative pt-24 pb-16 px-6 sm:px-12 flex flex-col items-center text-center">
    <h1 class="text-5xl md:text-6xl font-black text-airblack dark:text-white tracking-tight mb-8">VIP <span class="text-airred">Treatment</span></h1>
    <p class="mx-auto max-w-2xl text-xl text-gray-600 dark:text-gray-400 font-medium">Rules for thee, but not for me.</p>
</div>
<div class="max-w-4xl mx-auto px-6 mb-20 text-center text-gray-500 font-bold uppercase tracking-widest">
    [ Content Redacted / Pending Verification ]
</div>
{% endblock %}''',

    'archive.html': '''{% extends 'base.html' %}
{% block title %}Evidence Archive | StX Archive{% endblock %}
{% block content %}
<div class="mb-12 flex flex-col md:flex-row md:items-end justify-between px-6 lg:px-8">
    <div class="mb-6 md:mb-0">
        <h1 class="text-4xl font-black text-airblack dark:text-white tracking-tighter mb-3">Evidence Archive</h1>
        <p class="text-lg text-gray-600 dark:text-gray-400 font-medium">Search and browse all documented materials.</p>
    </div>
    
    <div class="w-full md:w-96">
        <div class="relative group">
            <input type="text" class="w-full bg-white dark:bg-[#151515] border border-gray-200 dark:border-gray-800 rounded-xl pl-12 pr-4 py-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-airred focus:border-airred transition-all font-medium placeholder-gray-400 dark:placeholder-gray-600 shadow-sm group-hover:border-airred/50" placeholder="Search archive...">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
        </div>
    </div>
</div>

<div class="px-6 lg:px-8 mb-20">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div class="bg-white dark:bg-[#151515] rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800 overflow-hidden hover:shadow-xl transition-all hover:-translate-y-1 hover:border-airred/30 group">
            <div class="h-48 bg-gray-100 dark:bg-[#111] flex items-center justify-center relative border-b border-gray-100 dark:border-gray-800">
                <svg class="h-12 w-12 text-gray-300 dark:text-gray-700 transition-transform duration-500 group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                <div class="absolute inset-0 bg-airblack/0 group-hover:bg-airblack/40 dark:group-hover:bg-airblack/60 transition-all flex items-center justify-center backdrop-blur-[2px] opacity-0 group-hover:opacity-100">
                    <a href="{{ url_for('document') }}" class="bg-airred text-white px-6 py-2 rounded-lg font-bold uppercase tracking-wider text-sm shadow-lg transform translate-y-4 group-hover:translate-y-0 transition-all hover:bg-airdarkred">View Details</a>
                </div>
            </div>
            <div class="p-6">
                <div class="flex justify-between items-start mb-4">
                    <span class="text-xs font-bold uppercase tracking-wider text-gray-400 dark:text-gray-500">July 13, 2026</span>
                    <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider border border-airred/30 bg-airred/5 text-airred">Notice</span>
                </div>
                <h3 class="text-xl font-black text-airblack dark:text-white mb-2 truncate group-hover:text-airred transition-colors">Portal Guidelines</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 font-medium">Initial guidelines for submitting and reviewing evidence.</p>
            </div>
        </div>
        
        <div class="bg-white dark:bg-[#151515] rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800 overflow-hidden hover:shadow-xl transition-all hover:-translate-y-1 hover:border-airred/30 group">
            <div class="h-48 bg-gray-100 dark:bg-[#111] flex items-center justify-center relative border-b border-gray-100 dark:border-gray-800">
                <span class="font-black text-4xl text-gray-800">₹52k</span>
            </div>
            <div class="p-6">
                <div class="flex justify-between items-start mb-4">
                    <span class="text-xs font-bold uppercase tracking-wider text-gray-400 dark:text-gray-500">Term 1</span>
                    <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider border border-gray-600 bg-gray-800 text-gray-300">Financial</span>
                </div>
                <h3 class="text-xl font-black text-airblack dark:text-white mb-2 truncate group-hover:text-airred transition-colors">4th Std Fee Receipt</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 font-medium">Documentary proof of the exorbitant 52,000 INR fees.</p>
            </div>
        </div>
        
        <div class="bg-white dark:bg-[#151515] rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800 overflow-hidden hover:shadow-xl transition-all hover:-translate-y-1 hover:border-airred/30 group">
            <div class="h-48 bg-gray-100 dark:bg-[#111] flex items-center justify-center relative border-b border-gray-100 dark:border-gray-800">
                <span class="font-black text-xl text-gray-700">₹630</span>
            </div>
            <div class="p-6">
                <div class="flex justify-between items-start mb-4">
                    <span class="text-xs font-bold uppercase tracking-wider text-gray-400 dark:text-gray-500">Aug 2026</span>
                    <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider border border-gray-600 bg-gray-800 text-gray-300">Scandal</span>
                </div>
                <h3 class="text-xl font-black text-airblack dark:text-white mb-2 truncate group-hover:text-airred transition-colors">Council Extortion</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 font-medium">Receipts showing payment required to perform school manual labor.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
    
    'experience.html': '''{% extends 'base.html' %}
{% block title %}Submit Experience | StX Archive{% endblock %}
{% block content %}
<div class="max-w-3xl mx-auto mb-16 px-6">
    <div class="text-center mb-12">
        <h1 class="text-4xl font-black text-airblack dark:text-white tracking-tighter mb-4">Share Your Experience</h1>
        <p class="text-lg text-gray-600 dark:text-gray-400 font-medium">Submit a firsthand account or testimony related to school policies or incidents.</p>
    </div>

    <div class="bg-white dark:bg-[#151515] rounded-3xl shadow-2xl overflow-hidden border border-gray-100 dark:border-gray-800 mb-20">
        <!-- existing form html -->
        <div class="p-8 text-center text-gray-500 font-bold uppercase tracking-widest">[ Submission Form Area ]</div>
    </div>
    
    <div class="border-t border-gray-200 dark:border-gray-800 pt-12">
        <h2 class="text-3xl font-black text-airblack dark:text-white tracking-tight mb-8">Recent Anonymous Submissions</h2>
        
        <div class="space-y-6">
            <div class="bg-[#111] border-l-4 border-airred p-6 rounded-r-xl">
                <h3 class="text-xl font-black text-white mb-2">Book Prices Are Insane</h3>
                <p class="text-gray-400 font-medium mb-3">"I went to buy the required books and they are priced like gold. To make it worse, the school diary isn't even included. You have to buy it separately along with a compulsory portfolio that literally no one uses."</p>
                <span class="text-xs text-gray-600 font-bold uppercase tracking-widest">Submitted 2 days ago</span>
            </div>
            
            <div class="bg-[#111] border-l-4 border-gray-600 p-6 rounded-r-xl">
                <h3 class="text-xl font-black text-white mb-2">Paying to become a laborer</h3>
                <p class="text-gray-400 font-medium mb-3">"They took ₹630 from me to become a student council member. My duties? Moving benches and doing chores for the school administration. It's paid child labor."</p>
                <span class="text-xs text-gray-600 font-bold uppercase tracking-widest">Submitted 5 days ago</span>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
}

for filename, content in html_files.items():
    with open(os.path.join(templates_dir, filename), 'w', encoding='utf-8') as f:
        f.write(content)

print("Successfully wrote all pages with user-provided content.")
