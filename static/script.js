// التحكم بالتمرير والواجهة
const wrapper = document.getElementById('main-slider');
const btnText = document.getElementById('btn-text');
const sections = ['hero', 'about', 'docs', 'editor'];

function scrollToSection(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth', 
        inline: 'start', 
        block: 'nearest' });
}

function nextSection() {
    const width = window.innerWidth;
    const currentIndex = Math.round(Math.abs(wrapper.scrollLeft) / width);
    scrollToSection(sections[(currentIndex + 1) % sections.length]);
}

wrapper.addEventListener('scroll', () => {
    const width = window.innerWidth;
    const activeIndex = Math.round(Math.abs(wrapper.scrollLeft) / width);

    const texts = ["استكشف اكثر", "تعرف على الدليل", "جرب المحرر الان!", "عودة للبداية"];
    if (btnText) btnText.innerText = texts[activeIndex] || "استكشف";

    // الوميض  على الزر 
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => btn.classList.remove('active'));
    if(navBtns[activeIndex]) {
        navBtns[activeIndex].classList.add('active');
    }

    // عند الانتقال لصفحة المحرر
    if (activeIndex === 3 && typeof editor !== 'undefined' && editor) {
        setTimeout(() => editor.refresh(), 100);
    }
});

// اعداد CodeMirror 
CodeMirror.defineSimpleMode("borhan", {
    start: [
        { regex: /"(?:[^\\]|\\.)*?(?:"|$)/, token: "string" },
        { regex: /'(?:[^\\]|\\.)*?(?:'|$)/, token: "string" },
        { regex: /(?:صحيح|عشري|نص|حرف|ثنائي|ارجع)(?![ا-يa-zA-Z0-9_])/, token: "keyword" },
        { regex: /(?:اذا|والا|بينما|كرر|نهاية|من|الى|اختر|حالة|افتراضي)(?![ا-يa-zA-Z0-9_])/, token: "keyword" },
        { regex: /(?:اطبع|ادخل)(?![ا-يa-zA-Z0-9_])/, token: "builtin" },
        { regex: /(?:صح|خطأ)(?![ا-يa-zA-Z0-9_])/, token: "keyword" },
        { regex: /!!.*/, token: "comment" },
        { regex: /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i, token: "number" },
        { regex: /==|!=|<=|>=|[-+\/*=<>]/, token: "operator" },
    ]
});

window.useExample = function(codeSnippet) {
    scrollToSection('editor');
    setTimeout(() => {
        if (editor) {
            editor.setValue(codeSnippet);
            editor.refresh();
            
            const runBtn = document.querySelector('.btn-run');
            if (runBtn) {
                runBtn.style.boxShadow = '0 0 30px var(--accent-primary)';
                setTimeout(() => {
                    runBtn.style.boxShadow = '0 5px 15px rgba(124,77,255,0.3)';
                }, 1500);
            }
        }
    }, 600);
};

let editor;
document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.getElementById("code");
    if (!textarea) return;

    editor = CodeMirror.fromTextArea(textarea, {
        mode: "borhan",
        theme: "ayu-dark",
        lineNumbers: true,
        lineWrapping: true,
        indentUnit: 4,
        matchBrackets: true,
        autoCloseBrackets: true,
        direction: "rtl",
        inputStyle: "contenteditable",
        rtlMoveVisually: true
    });

    const wrapper_el = editor.getWrapperElement();
    wrapper_el.style.direction = "rtl";
    wrapper_el.style.textAlign = "right";
    wrapper_el.style.height = "100%";
    wrapper_el.style.flex = "1";

    editor.setValue("!! اكتب كود بُرهان هنا\nصحيح س = 10 .\nاطبع س .");
    editor.refresh();

    editor.setOption("extraKeys", {
        "Ctrl-Enter": () => runCode()
    });
});

window.insertToEditor = function(codeSnippet) {
    if (editor) {
        editor.setValue(codeSnippet);
        scrollToSection('editor');
        setTimeout(() => editor.refresh(), 150);
    }
};

window.clearEditor = function() {
    if (editor) editor.setValue("");
};

window.clearTerminal = function() {
    const output = document.getElementById('output');
    output.innerHTML = 'انتظار البرهان...\n_';
    const dot = document.getElementById('status-dot');
    if (dot) {
        dot.style.background = '#444';
        dot.style.boxShadow = 'none';
    }
};

async function runCode() {
    if (!editor) {
        alert("المحرر غير جاهز بعد، انتظر لحظة.");
        return;
    }

    const code = editor.getValue();
    const output = document.getElementById('output');
    const dot = document.getElementById('status-dot');

    if (!code.trim()) {
        output.innerText = "الرجاء كتابة الكود اولا!";
        if (dot) dot.style.background = "var(--error)";
        return;
    }

    output.innerText = "جارِ تحليل الكود في مفسر بُرهان...";
    if (dot) {
        dot.style.background = "var(--warning)";
        dot.style.boxShadow = "0 0 10px var(--warning)";
    }

    try {
        const response = await fetch('/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });
        const data = await response.json();

        output.innerText = data.output + "\n\nاكتمل التنفيذ";

        const isError = data.output.includes("خطا") || data.output.toLowerCase().includes("error");
        if (dot) {
            dot.style.background = isError ? "var(--error)" : "var(--success)";
            dot.style.boxShadow = `0 0 10px ${isError ? 'var(--error)' : 'var(--success)'}`;
        }
    } catch (e) {
        output.innerText = "خطا: فشل الاتصال بمحرك بُرهان.\nالرجاء التاكد ان الخادم (Flask) يعمل حاليا.";
        console.error(e);
        if (dot) {
            dot.style.background = "var(--error)";
            dot.style.boxShadow = "0 0 10px var(--error)";
        }
    }
}

// جسيمات الخلفية بحركة عشوائية 
document.addEventListener("DOMContentLoaded", () => {
    const particlesContainer = document.getElementById('particles-container');
    const symbols = ['{ }', '[ ]', '=>', '</>', 'صحيح','.', 'اطبع س', '();','.','.', '*','.','نص', '/','!!', 'اذا','.','!!', 'عشري','بينما','0.5','.','+='];
    
    if(particlesContainer) {
        for(let i = 0; i < 40; i++) {
            let el = document.createElement('div');
            el.className = 'code-particle';
            el.innerText = symbols[Math.floor(Math.random() * symbols.length)];
            
            // توزيع البداية على كامل الشاشة
            el.style.left = Math.random() * 100 + 'vw';
            
            // سرعة عشوائية للصعود 
            const duration = (Math.random() * 40 + 25); 
            el.style.animationDuration = duration + 's';
            
            // تاخير عشوائي
            el.style.animationDelay = (Math.random() * 5) + 's';
            
            // حجم عشوائي
            el.style.fontSize = (Math.random() * 1.5 + 1) + 'rem';
            
            // انحراف عشوائي اثناء الصعود
            const randomMoveX = (Math.random() - 0.5) * 40; 
            el.style.setProperty('--move-x', randomMoveX + 'vw');
            
            particlesContainer.appendChild(el);
        }
    }
});
