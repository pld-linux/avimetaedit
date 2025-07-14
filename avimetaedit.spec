# TODO: system tinyxml2 and libzen
Summary:	Embed, validate and export AVI files metadata
Summary(pl.UTF-8):	Osadzanie, sprawdzanie i eksport metadanych z plików AVI
Name:		avimetaedit
Version:	1.0.2
Release:	1
License:	CC0 1.0 (Public Domain)
Group:		Applications/Multimedia
Source0:	https://mediaarea.net/download/source/avimetaedit/%{version}/%{name}_%{version}.tar.xz
# Source0-md5:	3282d203da2d5fc4c081a1ac38b67af0
Patch0:		%{name}-update.patch
URL:		https://mediaarea.net/AVIMetaEdit
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= 5
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AVI MetaEdit is a tool that supports embedding, validating, and
exporting of metadata in AVI (Standard and OpenDML) files. This tool
can also enforce file structure and metadata recommendations and
specifications from U.S. National Archives, Microsoft, and IBM.

%description -l pl.UTF-8
AVI MetaEdit to narzędzie obsługujące osadzanie, sprawdzanie
poprawności i eksportowanie metadanych w plikach AVI (standardowych i
OpenDML). Narzędzie potrafi wymusić strukturę i rekomendację
metadanych zgodne ze specyfikacjami U.S. National Archives,
Microsoftu i IBM-a.

%package gui
Summary:	GUI to embed, validate and export AVI files metadata
Summary(pl.UTF-8):	Graficzny interfejs użytkownika do osadzania, sprawdzania i eksportu metadanych z plików AVI
Group:		X11/Applications/Multimedia

%description gui
AVI MetaEdit to narzędzie obsługujące osadzanie, sprawdzanie
poprawności i eksportowanie metadanych w plikach AVI (standardowych i
OpenDML). Narzędzie potrafi wymusić strukturę i rekomendację
metadanych zgodne ze specyfikacjami U.S. National Archives,
Microsoftu i IBM-a.

%description gui -l pl.UTF-8
AVI MetaEdit to narzędzie obsługujące osadzanie, sprawdzanie
poprawności i eksportowanie metadanych w plikach AVI (standardowych i
OpenDML). Narzędzie potrafi wymusić strukturę i rekomendację
metadanych zgodne ze specyfikacjami U.S. National Archives,
Microsoftu i IBM-a.

%prep
%setup -q -n avimetaedit
%patch -P0 -p1
%undos *.html *.txt Release/*.txt
chmod 644 *.html *.txt Release/*.txt

%build
# build CLI
cd Project/GNU/CLI
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}
# now build GUI
cd ../../../Project/GNU/GUI
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
# Qt5Core with -reduce-relocations requires PIC code
%configure \
	CXXFLAGS="%{rpmcxxflags} -fPIC"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C Project/GNU/CLI install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C Project/GNU/GUI install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_datadir}/metainfo,%{_desktopdir},%{_iconsdir}/hicolor/128x128/apps}
cp -p Project/GNU/GUI/avimetaedit-gui.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p Project/GNU/GUI/avimetaedit-gui.metainfo.xml $RPM_BUILD_ROOT%{_datadir}/metainfo
cp -p Source/Resource/Image/Brand/Logo128.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/128x128/apps/avimetaedit.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc License.html History_CLI.txt README.md Release/ReadMe_CLI_Linux.txt
%attr(755,root,root) %{_bindir}/avimetaedit

%files gui
%defattr(644,root,root,755)
%doc License.html History_GUI.txt Release/ReadMe_GUI_Linux.txt
%attr(755,root,root) %{_bindir}/avimetaedit-gui
%{_datadir}/metainfo/avimetaedit-gui.metainfo.xml
%{_desktopdir}/avimetaedit-gui.desktop
%{_iconsdir}/hicolor/128x128/apps/avimetaedit.png
