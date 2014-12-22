%define beta beta2

Name:		freeciv
Version:	2.5.0
%if "%beta" != ""
Release:	0.%beta.1
Source0:	http://download.gna.org/freeciv/beta/freeciv-%version-%beta.tar.bz2
%else
Release:	1
Source0:	http://download.gna.org/freeciv/stable/freeciv-%version.tar.gz
%endif
Summary:	CIVilization clone
License:	GPLv2+
Group:		Games/Strategy
URL:		http://www.freeciv.org/
Source1:	%{name}.server.wrapper
Source2:	stdsounds3.tar.gz
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(SDL_gfx)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(gtk+-2.0)
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

%package	client
Group:		Games/Strategy
Summary:	FREE CIVilization clone - client
Provides:	%{name} = %{version}-%{release}
Requires:	%{name}-data = %{version}
Requires:	%{name}-server = %{version}
Obsoletes:	%{name}-client < %{version}-%{release}

%description	client
This is the graphical client for freeciv

%package	server
Group:		Games/Strategy
Summary:	FREE CIVilization clone - server
Provides:	%{name} = %{version}-%{release}
Requires:	%{name}-data = %{version}

%description	server
This is the server for freeciv.

%prep
%if "%beta" != ""
%setup -q -n %name-%version-%beta
%else
%setup -q
%endif

%build
#locales are not in %{_gamesdatadir}
export localedir=%{_datadir}/locale

%configure2_5x \
    --bindir=%{_gamesbindir} \
    --datadir=%{_gamesdatadir} \
    --enable-client=sdl
%make

%install
%__rm -rf %{buildroot}
%makeinstall_std localedir=%{_datadir}/locale

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

%find_lang %{name}
%find_lang freeciv-nations

#remove unneeded
# The Qt one will be useful as soon as the Qt client becomes more than a
# stub -- probably by 2.5.x
%__rm -f %{buildroot}%{_libdir}/*a
%__rm -f %{buildroot}%{_mandir}/man6/*ftwl*
%__rm -f %{buildroot}%{_mandir}/man6/freeciv-gtk2.6*
%__rm -f %{buildroot}%{_mandir}/man6/*gtk3*
%__rm -f %{buildroot}%{_mandir}/man6/*qt*
%__rm -f %{buildroot}%{_mandir}/man6/*win32*
%__rm -f %{buildroot}%{_mandir}/man6/*xaw*

%files -f %{name}.lang,freeciv-nations.lang data
%doc AUTHORS doc/BUGS doc/HOWTOPLAY NEWS doc/README doc/README.AI doc/README.graphics doc/README.rulesets doc/README.sound doc/HACKING
%{_gamesdatadir}/%{name}

%files client
%{_gamesbindir}/freeciv-sdl
%{_gamesbindir}/freeciv-manual
%{_gamesbindir}/freeciv-mp-gtk2
%{_mandir}/man6/freeciv-client.6*
%{_mandir}/man6/freeciv-mp-gtk2.6*
%{_mandir}/man6/freeciv-mp-cli.6*
%{_mandir}/man6/freeciv-sdl*
%{_mandir}/man6/freeciv-modpack*
%{_mandir}/man6/freeciv-manual*
%{_datadir}/applications/freeciv-sdl.desktop
%{_datadir}/applications/freeciv-mp-gtk2.desktop
%{_datadir}/appdata/*.xml
%{_datadir}/pixmaps/freeciv-client.png
%{_iconsdir}/hicolor/*/apps/freeciv-modpack.png
%{_iconsdir}/hicolor/*/apps/freeciv-client.png
%doc %{_docdir}/%{name}

%files server
%{_gamesbindir}/civserver.real
%{_gamesbindir}/freeciv-server
%{_mandir}/man6/freeciv-server.6*
%{_datadir}/applications/freeciv-server.desktop
%{_iconsdir}/hicolor/*/apps/freeciv-server.png
%_sysconfdir/freeciv
