%define	name	freeciv
%define version	2.1.0
%define rel	2
%define release %mkrel %{rel}

Name:		%{name}
Summary:	FREE CIVilization clone
Version:	%{version}
Release:	%{release}
Source0:	ftp://ftp.freeciv.org/freeciv/stable/%{name}-%{version}.tar.bz2
Source1:	%{name}.server.wrapper.bz2
Source2:	stdsounds2.tar.bz2
Source3:	%{name}.bash-completion.bz2
License:	GPL
Group:		Games/Strategy
BuildRequires:	SDL_mixer-devel gtk+2-devel ncurses-devel readline-devel
BuildRequires:	desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.freeciv.org/

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

%package        client
Group:          Games/Strategy
Summary:        FREE CIVilization clone - client
Provides:	%{name}
Obsoletes:	%{name}
Requires:	%{name}-data = %{version} %{name}-server = %{version}

%description    client
This is the graphical client for freeciv

%package        server
Group:          Games/Strategy
Summary:        FREE CIVilization clone - server
Provides:	%{name}
Obsoletes:	%{name}
Requires:	%{name}-data = %{version}

%description    server
This is the server for freeciv.

%prep
%setup -q
bzcat %{SOURCE3} > %{name}.bash-completion

%build
%configure2_5x \
    --bindir=%{_gamesbindir} \
    --datadir=%{_gamesdatadir} \
    --enable-client=gtk-2.0 
%make

%install
rm -rf %{buildroot}
%makeinstall_std localedir=%{_datadir}/locale

tar -jxf %{SOURCE2} -C %{buildroot}%{_gamesdatadir}/%{name}

# wrapper
mv %{buildroot}%{_gamesbindir}/civserver %{buildroot}%{_gamesbindir}/civserver.real
bzcat %{SOURCE1} > %{buildroot}%{_gamesbindir}/civserver
chmod 755 %{buildroot}%{_gamesbindir}/civserver

# fix icons locations
mv %{buildroot}%{_gamesdatadir}/icons %{buildroot}%{_datadir}/icons

# menu entry
perl -pi -e 's/\.png$//' %{buildroot}%{_datadir}/applications/*.desktop
desktop-file-install --vendor="" \
			--remove-category="Application" \
			--remove-category="GNOME" \
			--remove-category="Strategy" \
			--add-category="GTK" \
			--add-category="StrategyGame" \
			--dir %{buildroot}%{_datadir}/applications \
            %{buildroot}%{_datadir}/applications/*.desktop

%find_lang %{name}

install -m644 %{name}.bash-completion -D %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%post client
%update_menus

%postun client
%clean_menus

%post server
%update_menus

%postun server
%clean_menus

%clean
rm -rf %{buildroot}

%files -f %{name}.lang data
%defattr(-,root,root)
%doc AUTHORS doc/BUGS doc/HOWTOPLAY NEWS doc/README doc/README.AI doc/README.graphics doc/README.rulesets doc/README.sound doc/HACKING
%{_gamesdatadir}/%{name}
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}

%files client
%defattr(-,root,root)
%{_gamesbindir}/civclient
%{_gamesbindir}/civmanual
%{_mandir}/man6/civclient.6*
%{_datadir}/applications/freeciv.desktop
%{_datadir}/pixmaps/freeciv-client.png
%{_iconsdir}/hicolor/*/apps/freeciv-client.png

%files server
%defattr(-,root,root)
%{_gamesbindir}/civserver*
%{_mandir}/man6/civserver.6*
%{_datadir}/applications/freeciv-server.desktop
%{_iconsdir}/hicolor/*/apps/freeciv-server.png
