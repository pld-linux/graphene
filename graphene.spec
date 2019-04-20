# NOTE: despite some comments in configure, SSE2 is not selected at runtime;
# SSE2 option seems to change the ABI of library
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	introspection	# gobject introspection
%bcond_with	sse2		# x86 SSE2 fast paths
%bcond_without	armneon		# ARM NEON fast paths

%ifarch pentium4 %{x8664}
%define	with_sse2	1
%endif
Summary:	Graphene - a thin layer of types for graphic libraries
Summary(pl.UTF-8):	Graphene - cienka warstwa typów dla bibliotek graficznych
Name:		graphene
Version:	1.8.6
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/graphene/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	2f8bc12b1f4f764b7b547f0b85c932a3
Patch0:		%{name}-gir.patch
URL:		https://github.com/ebassi/graphene
%if %{with sse2}
BuildRequires:	gcc >= 6:4.9
%else
BuildRequires:	gcc >= 5:3.2
%endif
BuildRequires:	glib2-devel >= 1:2.40.0
%{?with_introspection:BuildRequires:	gobject-introspection-devel >= 1.41.0}
BuildRequires:	gtk-doc >= 1.20
BuildRequires:	meson >= 0.48.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
%{?with_introspection:BuildRequires:	python3 >= 1:3}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.40.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Graphene provides a small set of mathematical types needed to
implement graphic libraries that deal with 2D and 3D transformations
and projections.

%description -l pl.UTF-8
Graphene udostępnia mały zestaw typów matematycznych potrzebnych przy
implementowaniu bibliotek graficznych wykonujących przekształcenia i
rzuty 2D oraz 3D.

%package devel
Summary:	Header files for Graphene library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Graphene
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.40.0

%description devel
Header files for Graphene library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Graphene.

%package static
Summary:	Static Graphene library
Summary(pl.UTF-8):	Statyczna biblioteka Graphene
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Graphene library.

%description static -l pl.UTF-8
Statyczna biblioteka Graphene.

%package apidocs
Summary:	API documentation for Graphene library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Graphene
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Graphene library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Graphene.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	%{!?with_armneon:-Darm_neon=false} \
	-Dgtk_doc=true \
	%{!?with_introspection:-Dintrospection=false} \
	%{!?with_sse2:-Dsse2=false} \
	-Dtests=false

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libgraphene-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgraphene-1.0.so.0
%if %{with introspection}
%{_libdir}/girepository-1.0/Graphene-1.0.typelib
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgraphene-1.0.so
%{_includedir}/graphene-1.0
%dir %{_libdir}/graphene-1.0
%{_libdir}/graphene-1.0/include
%if %{with introspection}
%{_datadir}/gir-1.0/Graphene-1.0.gir
%endif
%{_pkgconfigdir}/graphene-1.0.pc
%{_pkgconfigdir}/graphene-gobject-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgraphene-1.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/graphene
