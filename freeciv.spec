%define _disable_ld_no_undefined 1

Name:		freeciv
Version:	3.0.0
Release:	1
Source0:	http://files.freeciv.org/stable/freeciv-%{version}.tar.xz
Summary:	CIVilization clone
License:	GPLv2+
Group:		Games/Strategy
URL:		http://www.freeciv.org/
Source1:	%{name}.server.wrapper
Source2:	http://files.freeciv.org/contrib/audio/stdsounds3.tar.gz
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(SDL2_gfx)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(SDL2_ttf)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
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
BuildArch:	noarch

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
Summary:	FREE CIVilization clone - Qt client
Requires:	%{name}-client-common = %{EVRD}
Provides:	%{name}-client = %{EVRD}

%description	client-qt
FREE CIVilization clone - Qt client

%package	client-sdl
Group:		Games/Strategy
Summary:	FREE CIVilization clone - SDL client
Requires:       %{name}-client-common = %{EVRD}
Provides:	%{name}-client = %{EVRD}

%description	client-sdl
FREE CIVilization clone - SDL client

%package	client-gtk
Group:		Games/Strategy
Summary:	FREE CIVilization clone - gtk client
Requires:       %{name}-client-common = %{EVRD}
Provides:	%{name}-client = %{EVRD}

%description	client-gtk
FREE CIVilization clone - gtk client

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
#locales are not in %{_gamesdatadir}
export localedir=%{_datadir}/locale

export CXXFLAGS="%{optflags} -std=gnu++14"
export PATH=%{_libdir}/qt5/bin:$PATH
%configure \
    --bindir=%{_gamesbindir} \
    --datadir=%{_gamesdatadir} \
    --enable-client=sdl2,qt \
    --with-qt5-includes=%{_includedir}/qt5
%make_build

%install
%__rm -rf %{buildroot}
%make_install localedir=%{_datadir}/locale

tar -xvf %{SOURCE2} -C %{buildroot}%{_gamesdatadir}/%{name}

# wrapper
%__mv %{buildroot}%{_gamesbindir}/freeciv-server %{buildroot}%{_gamesbindir}/civserver.real
%__install -m 755 %{SOURCE1} %{buildroot}%{_gamesbindir}/freeciv-server

# fix icons locations
%__mv %{buildroot}%{_gamesdatadir}/icons %{buildroot}%{_datadir}/icons

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
%{_gamesdatadir}/%{name}

%files client-common
%{_gamesbindir}/freeciv-manual
%{_gamesbindir}/freeciv-ruledit
%{_gamesbindir}/freeciv-ruleup
%{_datadir}/applications/org.freeciv.ruledit.desktop
%{_mandir}/man6/freeciv.6*
%{_mandir}/man6/freeciv-ruledit.6*
%{_mandir}/man6/freeciv-client.6*
%{_mandir}/man6/freeciv-mp-cli.6*
%{_mandir}/man6/freeciv-modpack*
%{_mandir}/man6/freeciv-manual*
%{_mandir}/man6/freeciv-ruleup.6*
%{_datadir}/appdata/*.xml
%{_datadir}/pixmaps/freeciv-client.png
%{_iconsdir}/hicolor/*/apps/freeciv-modpack.png
%{_iconsdir}/hicolor/*/apps/freeciv-client.png
%{_iconsdir}/hicolor/*x*/apps/freeciv-ruledit.png
%doc %{_docdir}/%{name}

%files client-sdl
%{_gamesbindir}/freeciv-sdl2
%{_datadir}/applications/org.freeciv.sdl2.desktop
%{_mandir}/man6/freeciv-sdl*

%files client-qt
%{_gamesbindir}/freeciv-qt
%{_datadir}/applications/org.freeciv.qt.desktop
%{_mandir}/man6/freeciv-mp-qt.6.*
%{_mandir}/man6/freeciv-qt.6.*

%files client-gtk
%{_gamesbindir}/freeciv-mp-gtk3
%{_mandir}/man6/freeciv-mp-gtk2.6*
%{_datadir}/applications/org.freeciv.mp.gtk3.desktop

%files server
%{_gamesbindir}/civserver.real
%{_gamesbindir}/freeciv-server
%{_mandir}/man6/freeciv-server.6*
%{_datadir}/applications/org.freeciv.server.desktop
%{_iconsdir}/hicolor/*/apps/freeciv-server.png
%_sysconfdir/freeciv
