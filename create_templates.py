import os

templates = {
    'policies.html': 'School Policies',
    'principals_note.html': 'Principal\'s Note',
    'incidents.html': 'Documented Incidents',
    'evidence_wall.html': 'The Evidence Wall',
    'hall_of_shame.html': 'Hall of Shame',
    'fee_scam.html': 'The Fee Scam',
    'vip_treatment.html': 'VIP Treatment'
}

base_content = '''{% extends 'base.html' %}

{% block title %}[TITLE] | StX Archive{% endblock %}

{% block content %}
<div class="relative pt-32 pb-16 px-6 sm:px-12 flex flex-col items-center text-center">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-airdarkred/20 via-transparent to-transparent opacity-50 dark:opacity-100 pointer-events-none"></div>
    
    <div class="relative z-10 w-full max-w-4xl">
        <div class="inline-block px-5 py-1 mb-12 rounded-full border border-airred/30 bg-transparent text-airred text-[11px] font-black tracking-[0.2em] uppercase">
            Section
        </div>
        
        <h1 class="text-[3rem] sm:text-5xl md:text-[4rem] font-black text-airblack dark:text-white tracking-tight mb-8 leading-[1.05]">
            [TITLE]
        </h1>
        
        <p class="mx-auto max-w-2xl text-lg sm:text-xl text-gray-600 dark:text-gray-400 mb-20 font-medium leading-relaxed">
            This section is currently being updated with new evidence. Please check back later.
        </p>
    </div>
</div>
{% endblock %}
'''

for filename, title in templates.items():
    with open(os.path.join('d:/Dev/black_ryan/templates', filename), 'w') as f:
        f.write(base_content.replace('[TITLE]', title))

print('Created templates')
