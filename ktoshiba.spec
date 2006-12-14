#
# Conditional build:
%bcond_without	synaptics	# don't build synaptics support
#
Summary:	KToshiba - Battery Monitor and Fn-Key support for Toshiba laptops
Summary(pl):	KToshiba - monitor baterii i obs³uga klawisza Fn dla laptopów Toshiby
Name:		ktoshiba
Version:	0.10
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/ktoshiba/%{name}-%{version}.tar.bz2
# Source0-md5:	41921887edd9fdd9c39c0f4ad77e435b
URL:		http://ktoshiba.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-qt-devel >= 0.62
BuildRequires:	kdelibs-devel >= 9:3.2.0
%{?with_synaptics:BuildRequires: libsynaptics-devel}
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Battery Monitor and Fn-Key support for Toshiba laptops.

%description -l pl
Monitor baterii oraz obs³uga skrótów klawiszowych Fn-X w laptopach
Toshiby.

%prep
%setup -q

%build
cp -f /usr/share/automake/config.sub admin
%{__make} -f admin/Makefile.common cvs

%configure \
%if "%{_lib}" == "lib64"
	--enable-libsuffix=64 \
%endif
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--with-qt-libraries=%{_libdir} \
	--with%{!?with_synaptics:out}-libsynaptics
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir} \
	kdelnkdir=%{_desktopdir} \

%find_lang %{name} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README README.MousePad README.omnibook ChangeLog
%attr(755,root,root) %{_bindir}/*
%{_libdir}/kde3/kcm_ktoshibam.la
%attr(755,root,root) %{_libdir}/kde3/kcm_ktoshibam.so
%{_libdir}/libktoshibaprocinterface.la
%attr(755,root,root) %{_libdir}/libktoshibaprocinterface.so.*.*.*
%{_libdir}/libktoshibasmminterface.la
%attr(755,root,root) %{_libdir}/libktoshibasmminterface.so.*.*.*
%{_libdir}/libktoshibaomnibookinterface.la
%attr(755,root,root) %{_libdir}/libktoshibaomnibookinterface.so.*.*.*
%{_desktopdir}/kde/%{name}*.desktop
%{_datadir}/autostart/ktoshiba.desktop
%{_iconsdir}/*/*/apps/%{name}.png
%{_datadir}/apps/%{name}
