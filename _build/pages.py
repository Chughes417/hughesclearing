"""Builds inner pages from the home page's shared header/footer.
Run:  python3 _build/pages.py   (from the site folder)
"""
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
home = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

head = home[:home.index('</head>')]
nav = home[home.index('<div class="nav-wrapper"'):home.index('<div class="hero-wrapper">')]
_js = home.index('<script>\n  // Nav turns')
footer = home[home.index('<div class="footer">'):_js]
script = home[_js:]
# drop home-only script pieces (tabs/video) — they are guarded below anyway
script = script.replace("const v=document.getElementById('background');\n  v.querySelector('source').addEventListener('error',()=>v.remove());",
                        "const v=document.getElementById('background');\n  if(v)v.querySelector('source').addEventListener('error',()=>v.remove());")


def relink(html, depth):
    """Prefix relative href/src with ../ for pages one folder down."""
    up = '../' * depth
    def fix(m):
        attr, q, url = m.group(1), m.group(2), m.group(3)
        if re.match(r'(https?:|tel:|mailto:|#|data:|javascript:|/)', url):
            return m.group(0)
        url = '' if url in ('./', '') else url
        return f'{attr}={q}{up}{url}{q}'
    return re.sub(r'(href|src|poster)=(["\'])([^"\']*)\2', fix, html)


def page(path, title, description, body):
    depth = path.count('/')
    h = head.replace('<title>Hughes Clearing | Land Clearing &amp; Dirt Work In Tyler, TX</title>',
                     f'<title>{title}</title>')
    h = re.sub(r'<meta name="description" content="[^"]*">',
               f'<meta name="description" content="{description}">', h)
    html = (h + '</head>\n<body class="home-body">\n\n' + nav + body + '\n' + footer + script)
    html = relink(html, depth)
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', path)


def page_header(h1, img=None):
    return (f'<div class="pageHeader"><div class="row text-center"><h1>{h1}</h1></div></div>\n')


ABOUT = page_header('About Us') + '''
<div class="contentMain">
  <div class="row">
    <h2>Dedicated To Quality Service</h2>
    <p>Your home, business, or pasture is more than just some piece of land. You have a lot of ideas for it–a vision that you’ve developed over the years. Hughes Clearing knows this. That’s why we work with each of our clients to figure out what they want for their land and then provide them with the services they need to achieve that vision. Hughes Clearing is a full-service land clearing, mulching, and excavation company, and we’re here to help you get the landscape you’ve always wanted.</p>
    <p><a class="button" href="contact-us/">Get A Quote</a></p>
  </div>

  <div class="edge-img-snippet2">
    <div class="box"><div class="edge-img-text">
      <h2>100% Satisfaction Guarantee</h2>
      <p>Hughes Clearing is dedicated to the kind of old-fashioned customer service you expect from a locally-owned and operated company. We include our customers in every aspect of the project. When we visit your property we meet with you to learn about your vision for the land. As we work, we check in with you to see if you like the direction. We also offer a 100% customer satisfaction guarantee. If you aren’t happy with our work, we’ll keep working until you are.</p>
      <p><a class="button" href="contact-us/">Get A Quote</a></p>
    </div></div>
    <div class="edge-img"><img src="images/about-guarantee.jpg" alt="" onerror="this.remove()"></div>
  </div>

  <div class="row"><h2 style="text-align:center">Our Core Values</h2></div>
  <div class="row">
    <ul class="blue-blocks">
      <li><div class="blue-block"><h3>Quality</h3><p>We do the job the right way, every time. We never cut corners to get to another job. You can trust we’ve taken the time to do it the best way.</p></div></li>
      <li><div class="blue-block"><h3>Service</h3><p>We’re dedicated to providing the kind of customer service that’s hard to find these days. We work until you think the job is perfect.</p></div></li>
      <li><div class="blue-block"><h3>Efficiency</h3><p>We understand that every one of our customers has a deadline to get their land cleared. We always take that seriously and get to you quickly.</p></div></li>
    </ul>
  </div>
</div>
'''

CONTACT = page_header('Contact Us') + '''
<div class="contentMain">
  <div class="row contact-grid">
    <div>
      <p><strong>Phone</strong><br><a href="tel:9032459344">(903) 245-9344</a></p>
      <p><strong>E-Mail</strong><br><a href="mailto:Info@HughesClearing.com">Info@HughesClearing.com</a></p>
      <p><strong>Mailing Address</strong><br>6146 CR 2297<br>Whitehouse, Texas 75791</p>
      <p><strong>Operating Hours</strong><br>Monday-Friday: 8am-5pm<br>Saturday: 10am-5pm</p>
    </div>
    <div>
      <!-- To have submissions emailed to you automatically, set data-endpoint to a form
           service URL (for example a Formspree form: https://formspree.io/f/XXXXXXX).
           Left blank, Submit opens the visitor's email app pre-filled to Info@HughesClearing.com. -->
      <form id="ContactForm" data-endpoint="" data-to="Info@HughesClearing.com" novalidate>
        <label>Name<input type="text" name="name"></label>
        <div class="form-row">
          <label>Email*<input id="email" type="email" name="email" required></label>
          <label>Phone<input type="tel" name="phone"></label>
        </div>
        <label>Message<textarea rows="5" name="message"></textarea></label>
        <br>
        <button type="submit" class="button" id="submitButton">Submit</button>
        <p class="form-status" id="formStatus" role="status"></p>
      </form>
    </div>
  </div>
</div>
<script>
(function(){
  const f=document.getElementById('ContactForm'),st=document.getElementById('formStatus');
  f.addEventListener('submit',async e=>{
    e.preventDefault();
    const email=f.email.value.trim();
    if(!email||!f.email.checkValidity()){st.textContent='Please enter a valid email address.';f.email.focus();return;}
    const d=Object.fromEntries(new FormData(f));
    const ep=f.dataset.endpoint;
    if(ep){
      st.textContent='Sending…';
      try{
        const r=await fetch(ep,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)});
        if(r.ok){f.reset();st.textContent='Thanks! We received your message and will be in touch soon.';}
        else st.textContent='Something went wrong. Please call (903) 245-9344.';
      }catch(_){st.textContent='Something went wrong. Please call (903) 245-9344.';}
    }else{
      const body=`Name: ${d.name||''}\\nEmail: ${d.email}\\nPhone: ${d.phone||''}\\n\\n${d.message||''}`;
      location.href=`mailto:${f.dataset.to}?subject=${encodeURIComponent('Website inquiry from '+(d.name||d.email))}&body=${encodeURIComponent(body)}`;
      st.textContent='Opening your email app…';
    }
  });
})();
</script>
'''

page('about-us/index.html', 'About Us - Hughes Clearing Co.',
     'You have a vision for your property, and Hughes Clearing is the professional excavation and land clearing company that can make it happen.',
     ABOUT)
page('contact-us/index.html', 'Contact Us - Hughes Clearing Co.',
     'Contact Hughes Clearing Co. for land clearing, forestry mulching, brush hogging and dirt work in Tyler and East Texas. Call (903) 245-9344.',
     CONTACT)
