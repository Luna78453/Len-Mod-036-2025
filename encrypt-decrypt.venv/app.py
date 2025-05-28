import ecdc
from waitress import server

serve(ecdc, host='0.0.0.0', port=5000)
