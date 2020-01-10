%global debug_package %{nil}

%define major 1
%define libname %mklibname osmpbf %{major}
%define devname %mklibname osmpbf -d

Name: osmpbf
Version: 1.3.3
Release: 2
Source0: https://github.com/scrosby/OSM-binary/archive/master.tar.gz
Patch0: osmpbf-build-shared-library.patch
Summary: Library for handling OpenStreetMap PBF files
URL: http://github.com/scrosby/OSM-binary
License: GPLv3
Group: System/Libraries
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: pkgconfig(protobuf-lite)

%description
Library for handling OpenStreetMap PBF files

%package -n %{libname}
Summary: Library for handling OpenStreetMap PBF files
Group: System/Libraries

%description -n %{libname}
Library for handling OpenStreetMap PBF files

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%setup -qn OSM-binary-master
%autopatch -p1

%if "%{_lib}" != "lib"
find . -name CMakeLists.txt |xargs sed -i -e "s,DESTINATION lib,DESTINATION %{_lib},g"
%endif

%cmake -G Ninja

%build
%ninja -C build

%install
%ninja_install -C build
mkdir -p %{buildroot}%{_mandir}/man1
install -c -m 644 tools/osmpbf-outline.1 %{buildroot}%{_mandir}/man1

%files
%{_bindir}/osmpbf-outline
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
