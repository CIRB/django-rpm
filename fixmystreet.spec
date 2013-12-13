Name:	        fixmystreet	
Version:	%{version}
Release:	1%{?dist}
Summary:	Django fixmystreet
Group:		Applications/System
License:	GNU Affero General Public License
URL:		https://github.com/CIRB/django-fixmystreet
Source0:        https://github.com/CIRB/django-fixmystreet/archive/%{version}.tar.gz	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  python27, python27-distribute, python27-virtualenv
BuildRequires:  libxml2-devel, gettext, libjpeg-devel, zlib-devel
Requires:       python27, python27-distribute, python27-virtualenv, python27-gunicorn, python27-psycopg2
Requires:       gdal, gdal-python, geos, proj, hdf5
Requires:       python-imaging, urw-fonts, wkhtmltoimage-static, wkhtmltopdf-static
AutoReqProv:    no

%define installdir /data/%{name}
%define virtualenv virtualenv-2.7
#%define __prelink_undo_cmd %{nil}

%description


%prep
tar xvzf %{_sourcedir}/%{version}

%build
rm -rf $RPM_BUILD_ROOT || true
mkdir -p $RPM_BUILD_ROOT/data
cp -r django-fixmystreet-%{version} $RPM_BUILD_ROOT%{installdir}


%install
%{virtualenv} --system-site-packages $RPM_BUILD_ROOT%{installdir}
cd $RPM_BUILD_ROOT%{installdir}
$RPM_BUILD_ROOT%{installdir}/bin/python2.7 setup.py install
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/bin/*
rm $RPM_BUILD_ROOT%{installdir}/.gitignore

%clean
rm -rf %{buildroot}

%pre
/usr/bin/getent passwd %{name} >/dev/null 2>&1 || userdel %{name} >/dev/null 2>&1
/usr/bin/getent passwd %{name} >/dev/null 2>&1 || useradd -r %{name} -u 600 -d %{installdir} -s /bin/bash >/dev/null 2>&1

%post
cd %{installdir} && bin/manage.py migrate --all
cd %{installdir} && bin/manage.py collectstatic --noinput

%postun
userdel %{name} >/dev/null 2>&1

%files
%defattr(-,%{name},%{name},-)
%doc
%{installdir}

%changelog
* Fri Dec 13 2013 Jean-Francois Roche <jfroche@affinitic.be>
- Initial RPM release
