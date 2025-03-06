import subprocess

def test_add():
	res = subprocess.run("./build/app.exe", input="10+15", text=True, capture_output=True)
	assert res.returncode == 0
	assert int(res.stdout) == 25

def test_mult():
	res = subprocess.run("./build/app.exe", input="5 * 5", text=True, capture_output=True)
	assert res.returncode == 0
	assert int(res.stdout) == 25
	
def test_del():
	res = subprocess.run("./build/app.exe", input="100 / 4", text=True, capture_output=True)
	assert res.returncode == 0
	assert int(res.stdout) == 25
	
def test_minus():
	res = subprocess.run("./build/app.exe", input="39 - 14", text=True, capture_output=True)
	assert res.returncode == 0
	assert int(res.stdout) == 25
	
def test_brackeds():
	res = subprocess.run("./build/app.exe", input="((10+15))", text=True, capture_output=True)
	assert res.returncode == 0
	assert int(res.stdout) == 25
	
def test_spaces():
	res = subprocess.run("./build/app.exe", input="39        \t\f\r\n- 14", text=True, capture_output=True)
	assert res.returncode == 0
	assert int(res.stdout) == 25
	
def test_float():
	res = subprocess.run(["./build/app.exe", "--float"], input="26/4", text=True, capture_output=True)
	assert res.returncode == 0
	assert float(res.stdout) == 6.5000
	
def test_paried_bracked():
	res = subprocess.run("./build/app.exe", input="(10+15", text=True, capture_output=True)
	assert res.returncode != 0
	
def test_empty_input ():
	res = subprocess.run("./build/app.exe", input="", text=True, capture_output=True)
	assert res.returncode != 0
	
def test_invalid_argument ():
	res = subprocess.run(["./build/app.exe", "-float"], input="10+15", text=True, capture_output=True)
	assert res.returncode != 0
	
def test_unknown_character ():
	res = subprocess.run("./build/app.exe", input="10 + 15a", text=True, capture_output=True)
	assert res.returncode != 0
	
def test_multy_operands ():
	res = subprocess.run("./build/app.exe", input="10 10+15", text=True, capture_output=True)
	assert res.returncode != 0
	
def test_multy_operators ():
	res = subprocess.run("./build/app.exe", input="+10+15", text=True, capture_output=True)
	assert res.returncode != 0
	
def test_null_division ():
	res = subprocess.run("./build/app.exe", input="10/0", text=True, capture_output=True)
	assert res.returncode != 0
