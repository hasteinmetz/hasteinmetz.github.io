---
layout: default
title: Contact Me
description: A page with a form to reach out to me
tag: navbar mail
---
<h2>{{page.title: Coming soon!}}</h2>
<!--
<h2>{{page.title}}</h2>
<div class="container">
  <div class="block"></div>
  <div class="block"></div>
  <div class="block"></div>
  <div class="block"></div>
  <div class="block"></div>
</div>

<a id="mail">

<div class="email">
  <form id="mail" method="post" enctype="text/plain">
  <script type="text/javascript" language="javascript">
  <!--
  // Email obfuscator script 2.1 by Tim Williams, University of Arizona
  // Random encryption key feature coded by Andrew Moulden
  // This code is freeware provided these four comment lines remain intact
  // A wizard to generate this code is at http://www.jottings.com/obfuscator/
  { coded = "3chch3@dELeK.IhE"
    key = "oIzNl5M8BAnjFDCxhtkmK4qgOJpsWf9y3Y1EaGUdiR7PQV6cwbu2LTXZeHv0rS"
    shift=coded.length
    link=""
    for (i=0; i<coded.length; i++) {
      if (key.indexOf(coded.charAt(i))==-1) {
        ltr = coded.charAt(i)
        link += (ltr)
      }
      else {     
        ltr = (key.indexOf(coded.charAt(i))-shift+key.length) % key.length
        link += (key.charAt(ltr))
      }
    }
    var strlink = "mailto:" + link
  document.getElementById("mail").setAttribute("action",strlink);
  }
  //--><!--
  </script>
  <noscript>Sorry, you need Javascript on to email me.</noscript>
  Name:<br>
  <input type="text" name="name"><br>
  E-mail:<br>
  <input type="text" name="mail"><br>
  Message:<br>
  <input type="text" name="comment" size="80" style="line-height:80px; valign:top"><br><br>
  <input type="submit" value="Send">
  <input type="reset" value="Reset">
  </form>
</div>

<div class="container">
  <div class="block"></div>
  <div class="block"></div>
  <div class="block"></div>
  <div class="block"></div>
  <div class="block"></div>
</div>
