%define _disable_ld_no_undefined 1

Name:		freeciv
Version:	3.2.0
Release:	1
Source0:	https://files.freeciv.org/stable/freeciv-%{version}.tar.xz
Summary:	CIVilization clone
License:	GPLv2+
Group:		Games/Strategy
URL:		https://www.freeciv.org/
Source1:	%{name}.server.wrapper
Source2:	https://files.freeciv.org/contrib/audio/stdsounds3.tar.gz
BuildRequires:	gettext
BuildRequires:	meson
BuildRequires:	locales-extra-charsets
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(SDL2_gfx)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(SDL2_ttf)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Linguist)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	readline-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libstdc++-static-devel

%description
Freeciv is a multiplayer strategy game, released under the GNU General
Public License. It is generally comparable with Civilization II(r),
published by Microprose(r).

Default configuration uses the Civilization II(r) style Isometric view. If
you prefer classic Civilization(r) 2-d view, invoke the client with
"civclient --tiles trident".

%package	data
Group:		Games/Strategy
Summary:	FREE CIVilization clone - data files
Requires:	%{name}-server = %{version}

%description	data
Freeciv is a multiplayer strategy game, released under the GNU General
Public License. It is generally comparable with Civilization II(r),
published by Microprose(r).

Default configuration uses the Civilization II(r) style Isometric view. If
you prefer classic Civilization(r) 2-d view, invoke the client with
"civclient --tiles trident".

%package	client-common
Group:		Games/Strategy
Summary:	FREE CIVilization clone - client
Provides:	%{name} = %{version}-%{release}
Requires:	%{name}-data = %{version}
Requires:	%{name}-server = %{version}
Requires:	%{name}-client = %{EVRD}
Suggests:	%{name}-client-sdl = %{EVRD}
Obsoletes:	%{name}-client < %{version}-%{release}

%description	client-common
This is the graphical client for freeciv

%package	client-qt
Group:		Games/Strategy
Summary:	FREE CIVilization clone - Qt6 client
Requires:	%{name}-client-common = %{EVRD}
Provides:	%{name}-client = %{EVRD}

%description	client-qt
FREE CIVilization clone - Qt6 client

%package	client-sdl
Group:		Games/Strategy
Summary:	FREE CIVilization clone - SDL client
Requires:       %{name}-client-common = %{EVRD}
Provides:	%{name}-client = %{EVRD}

%description	client-sdl
FREE CIVilization clone - SDL client

%package	client-gtk
Group:		Games/Strategy
Summary:	FREE CIVilization clone - gtk3 client
Requires:       %{name}-client-common = %{EVRD}
Provides:	%{name}-client = %{EVRD}

%description	client-gtk
FREE CIVilization clone - gtk3 client

%package	client-gtk4
Group:		Games/Strategy
Summary:	FREE CIVilization clone - gtk4 client
Requires:       %{name}-client-common = %{EVRD}
Provides:	%{name}-client = %{EVRD}

%description	client-gtk4
FREE CIVilization clone - gtk4 client

%package	server
Group:		Games/Strategy
Summary:	FREE CIVilization clone - server
Provides:	%{name} = %{version}-%{release}
Requires:	%{name}-data = %{version}

%description	server
This is the server for freeciv.

%prep
%setup -q

%build
%meson \
	-Dack_experimental=true \
	-Dclients=sdl2,gtk3.22,gtk4,qt \
	-Dfcmp=gtk4,gtk3,cli,qt \
 	-Daudio=true \
  	-Dqtver=qt6 \
   	-Dserver=enabled
%meson_build

%install
%meson_install

#tar -xvf %{SOURCE2} -C %{buildroot}%{_gamesdatadir}/%{name}

# wrapper
#__mv %{buildroot}%{_gamesbindir}/freeciv-server %{buildroot}%{_gamesbindir}/civserver.real
#__install -m 755 %{SOURCE1} %{buildroot}%{_gamesbindir}/freeciv-server

# fix icons locations
#__mv %{buildroot}%{_gamesdatadir}/icons %{buildroot}%{_datadir}/icons

# menu entry
desktop-file-install --vendor="" \
			--remove-category="Application" \
			--remove-category="GNOME" \
			--remove-category="SDL" \
			--remove-category="Strategy" \
			--add-category="X-SDL" \
			--add-category="StrategyGame" \
			--dir %{buildroot}%{_datadir}/applications \
            %{buildroot}%{_datadir}/applications/*.desktop

%find_lang %{name}-core
%find_lang freeciv-nations
%find_lang freeciv-ruledit

#remove unneeded
# The Qt one will be useful as soon as the Qt client becomes more than a
# stub -- probably by 2.5.x
%__rm -f %{buildroot}%{_libdir}/*a
%__rm -f %{buildroot}%{_mandir}/man6/*ftwl*
%__rm -f %{buildroot}%{_mandir}/man6/freeciv-gtk2.6*
%__rm -f %{buildroot}%{_mandir}/man6/*gtk3*
%__rm -f %{buildroot}%{_mandir}/man6/*win32*
%__rm -f %{buildroot}%{_mandir}/man6/*xaw*

%files -f %{name}-core.lang -f freeciv-nations.lang -f freeciv-ruledit.lang data
%doc AUTHORS doc/BUGS doc/HOWTOPLAY NEWS doc/README doc/README.AI doc/README.graphics doc/README.rulesets doc/README.sound doc/HACKING
%{_datadir}/freeciv/
%{_libdir}/libfreeciv.so

%files client-common
%{_bindir}/freeciv-manual
%{_bindir}/freeciv-mp-cli
%{_bindir}/freeciv-ruleup
%{_mandir}/man6/freeciv-client.6*
#{_mandir}/man6/freeciv-gtk3.22.6*
%{_mandir}/man6/freeciv-gtk4.6*
%{_mandir}/man6/freeciv-manual.6*
%{_mandir}/man6/freeciv-modpack.6*
%{_mandir}/man6/freeciv-mp-cli.6*
#{_mandir}/man6/freeciv-mp-gtk3.6*
%{_mandir}/man6/freeciv-mp-gtk4.6*
%{_mandir}/man6/freeciv-mp-qt.6*
%{_mandir}/man6/freeciv-qt.6*
%{_mandir}/man6/freeciv-ruledit.6*
%{_mandir}/man6/freeciv-ruleup.6*
%{_mandir}/man6/freeciv-sdl2.6*
%{_mandir}/man6/freeciv-server.6*
%{_mandir}/man6/freeciv.6*
%{_datadir}/metainfo/org.freeciv*
%{_iconsdir}/hicolor/*/apps/freeciv-modpack.png
%{_iconsdir}/hicolor/*/apps/freeciv-client.png
%{_iconsdir}/hicolor/*x*/apps/freeciv-ruledit.png
%doc %{_docdir}/%{name}

%files client-sdl
%{_bindir}/freeciv-sdl2
%{_datadir}/applications/org.freeciv.sdl2.desktop

%files client-qt
%{_bindir}/freeciv-qt
%{_bindir}/freeciv-mp-qt
%{_datadir}/applications/org.freeciv.qt.desktop
%{_datadir}/applications/org.freeciv.qt.mp.desktop

%files client-gtk
%{_bindir}/freeciv-gtk3.22
%{_bindir}/freeciv-mp-gtk3
%{_datadir}/applications/org.freeciv.gtk3.mp.desktop
%{_datadir}/applications/org.freeciv.gtk322.desktop

%files client-gtk4
%{_bindir}/freeciv-gtk4
%{_bindir}/freeciv-mp-gtk4
%{_datadir}/applications/org.freeciv.gtk4.desktop
%{_datadir}/applications/org.freeciv.gtk4.mp.desktop

%files server
%{_bindir}/freeciv-server
%{_datadir}/applications/org.freeciv.server.desktop
%{_iconsdir}/hicolor/*x*/apps/freeciv-server.png
%{_sysconfdir}/freeciv/database.lua
