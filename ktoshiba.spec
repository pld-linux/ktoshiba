%bcond_without	synaptics	# don't build synaptics support

Summary:	KToshiba
Summary(pl):	KToshiba
Name:		ktoshiba
Version:	0.9
Release:	0.2
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/ktoshiba/%{name}-%{version}.tar.bz2
# Source0-md5:	fa5d84245adc38d13199bad658ec0cea
URL:		http://ktoshiba.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	kdelibs-devel >= 9:3.2.0
%{?with_synaptics:BuildRequires: libsynaptics-devel}
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Battery Monitor and Fn-Key support for Toshiba laptops.

%description -l pl
Monitor baterii oraz wsparcie dla skrótów klawiszowych Fn-X w
laptopach Toshiba.

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
%attr(755,root,root) %{_libdir}/libktoshibaprocinterface.so.0.0.0
%{_libdir}/libktoshibasmminterface.la
%attr(755,root,root) %{_libdir}/libktoshibasmminterface.so.0.0.0
%{_datadir}/autostart/ktoshiba.desktop
%{_desktopdir}/*
%{_iconsdir}/*/*/apps/%{name}.png
%{_datadir}/apps/%{name}
