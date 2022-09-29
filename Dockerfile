FROM python:3.8.3
# Simple docker file for developer testing not intended for any deployment strategy 
 
ENV http_proxy http://proxy-chain.intel.com:911
ENV https_proxy http://proxy-chain.intel.com:912
ENV socks_proxy http://proxy-chain.intel.com:1080
ENV no_proxy intel.com,.intel.com,10.0.0.0/8,192.168.0.0/16,localhost,127.0.0.0/8,134.134.0.0/16
EXPOSE 8080

#Install required python packages for Autoflow
RUN pip install flask==0.12
RUN pip install alembic==1.7.4
RUN pip install bcrypt==3.2.0
RUN pip install cffi==1.14.6
RUN pip install click==6.6
RUN pip install colorama==0.4.4
RUN pip install coverage==4.2
RUN pip install cryptography==35.0.0
RUN pip install Flask-Bcrypt==0.7.1
RUN pip install Flask-Cors==3.0.10
RUN pip install Flask-Migrate==2.0.2
RUN pip install Flask-MySQLdb==0.2.0
RUN pip install Flask-Script==2.0.5
RUN pip install Flask-SQLAlchemy==2.1
RUN pip install Flask-Testing==0.6.1
RUN pip install greenlet==1.1.2
RUN pip install importlib-metadata==4.8.1
RUN pip install importlib-resources==5.2.2
RUN pip install itsdangerous==0.24
RUN pip install Jinja2==2.8
RUN pip install Mako==1.0.6
RUN pip install MarkupSafe==0.23
RUN pip install mysql-connector-python==8.0.26
RUN pip install mysqlclient==2.0.3
RUN pip install numpy==1.21.2
RUN pip install pandas==1.3.3
RUN pip install protobuf==3.18.1
RUN pip install pycparser==2.17
RUN pip install PyJWT==1.4.2
RUN pip install PyMySQL==1.0.2
RUN pip install python-dateutil==2.8.2
RUN pip install python-editor==1.0.3
RUN pip install pytz==2021.3
RUN pip install six==1.10.0
RUN pip install SQLAlchemy==1.3.24
RUN pip install Werkzeug==0.16.1
RUN pip install zipp==3.6.0
RUN pip install gunicorn==20.1.0
RUN pip install requests==2.23.0
RUN pip install websocket-client==0.57.0
RUN pip install websockets==8.1
RUN pip install python-dotenv==0.17.0

#Create Autoflow directory and copy api repo 
RUN mkdir -p /usr/oap_service
WORKDIR /usr/oap_service
COPY . .

CMD ["python", "swagger_api.py"]


#Build with name: oap_services:v0.1
#docker tag oap_services:v0.1 amr-registry.caas.intel.com/owr/platform_automation/autoflow/linux:oap_services_0.1
#docker push amr-registry.caas.intel.com/owr/platform_automation/autoflow/linux:oap_services_0.1