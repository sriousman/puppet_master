

# Example of Custom Wait Condition
class element_has_css_class(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, css_class):
    self.locator = locator
    self.css_class = css_class

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if self.css_class in element.get_attribute("class"):
        return element
    else:
        return False

# Wait until an element with id='myNewInput' has class 'myCSSClass'
wait = WebDriverWait(driver, 10)
element = wait.until(element_has_css_class((By.ID, 'myNewInput'), "myCSSClass"))



# Explicit Wait
driver = webdriver.Firefox()
driver.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
finally:
    driver.quit()


# Predefined Conditions
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))

#Implicit Waits
driver = webdriver.Firefox()
driver.implicitly_wait(10) # seconds
driver.get("http://somedomain/url_that_delays_loading")
myDynamicElement = driver.find_element_by_id("myDynamicElement")


## cgi-bin/bbw.sh?pgm=APPL.UPL&insname=Puppet%2C+Master&downpay=293.00+++&key=180319+PUPPET&payMethod=Check&payNumber=money+money+money!!
##/cgi-bin/pdf_retriever.py?key=180319 PUPPET&pdftype=okletter&printid=01&agent=5121
##/cgi-bin/pdf_retriever.py?key=180319 PUPPET&pdftype=receipt&printid=01&agent=5121
##cgi-bin/pdf_retriever.py?key=180319 PUPPET&pdftype=um&printid=01&agent=5121
## i-bin/pdf_retriever.py?key=180319 PUPPET&pdftype=svcard&printid=01&agent=5121
##cgi-bin/pdf_retriever.py?key=180319 PUPPET&pdftype=appl&printid=01&agent=5121
## cgi-bin/qrw.entry.py?mode=rewrite&key=N35017174&agent=5121&expdate=061818
<div id="prem"><div class="yui-panel-container shadow" id="panel1_c" style="visibility: visible; left: 691px; top: 1146px; z-index: 6;"><div id="panel1" class="yui-module yui-overlay yui-panel" style="visibility: inherit; width: 520px;" tabindex="0"><a class="container-close" href="#">Close</a><div class="hd" style="cursor: auto;">Rewrite Rating</div><div class="bd"><!-- Premium table from SUBR.QQ.PREM -->
<div style="text-align: center;">
  <table style="clear: both; margin-left: auto; margin-right: auto; text-align: left;">
    <thead>
      <tr><th></th></tr>
    </thead>
    <tbody>
      <!-- Restrictions -->
      <!-- Payments -->
      <tr class="">
        <td style="text-align: left; padding-right: 20px;"></td>
        <td class="ra" style="padding-right: 20px;">Down Pay</td>
        <td style="text-align: center; padding-right: 10px;"># of Pmts</td>
        <td class="ra">Payment Amt.</td>
        <td class="ra">Total</td>
      </tr>
      <tr class="">
        <td style="text-align: left; padding-right: 20px;">Full Pay</td>
        <td class="ra" style="padding-right: 20px;"> 1154.74</td>
        <td style="text-align: center; padding-right: 10px;"></td>
        <td class="ra">0.00</td>
        <td class="ra"> 1154.74</td>
      </tr>
      <tr class="">
        <td style="text-align: left; padding-right: 20px;">1/6 Down</td>
        <td class="ra" style="padding-right: 20px;"> 223.00</td>
        <td style="text-align: center; padding-right: 10px;">5</td>
        <td class="ra"> 209.00</td>
        <td class="ra">1214.20</td>
      </tr>
      <tr>
        <td>
          <form id="reqform" method="post" action="/cgi-bin/qrw_request.py">
            <input id="agent" name="agent" value="5121" type="hidden">
            <input id="vkey" name="vkey" value="N35017174" type="hidden">
            <input id="vexpdate" name="vexpdate" value="061818" type="hidden">
            <input name="dv31" value="6122416" type="hidden">
            <input name="addlpol" id="addlpol" value="N" type="hidden">
            <input name="mc" id="mc" value="N" type="hidden">
            <input id="seq" name="seq" value="0001" type="hidden">
            <input id="mode" name="mode" value="rewrite" type="hidden">
            <input id="dcmatch" name="dcmatch" value="DDD1" type="hidden">
            <input id="dummy" name="dummy" value="1" type="hidden">
          </form>
        </td>
      </tr>
    </tbody>
  </table>
  <br>
  <span class="footnote" style="font-size: x-small">This is a quote only and is subject to complete, accurate information and underwriting acceptability</span>
  <input id="portnum" name="portnum" value="3532A0" type="hidden">
</div>

</div><div class="ft"><div style="text-align: center;"><button id="edit">Edit Quote</button><button id="detail">Quote Detail</button><button id="printbox">Print</button><button id="reqsubmit">Submit Rewrite</button><button id="close">Close</button></div></div></div><div class="underlay"></div></div></div>