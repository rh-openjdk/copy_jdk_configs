#########################################################################
# this is using more config files then c-j-c are watching               #
# see the list and adjust c-j-c.lua!!!                                  #
# only add files in jvmdir, files in etc should be handled automagicaly #
#########################################################################
%global __jar_repack 0


%define javaver     10
%define etcjavasubdir     /etc/java/java-%{javaver}-openjdk
%define etcjavadir        %{etcjavasubdir}/%{uniquesuffix}
%define javaver_alternatives	1.10.0
%define	origin	super
%define priority 100000

%define buildver 1
%define purename	java-%{javaver}-%{origin}
%define version		%{javaver}.%{buildver}
%define release		1%{?dist}
%define uniquesuffix	%{purename}-%{version}.%{release}.%{_arch}

%define	sdkdir			%{uniquesuffix}

%define sdklibdir       %{_jvmdir}/%{sdkdir}/lib
%define jredir          %{sdkdir}/jre
%define jrelnk_versionless_name		jre-%{javaver}-%{origin}.%{_arch}
%define sdklnk_versionless_name		%{purename}.%{_arch}
%define sdk_versionless_bindir       	%{_jvmdir}/%{sdklnk_versionless_name}/bin
%define jre_versionless_bindir       	%{_jvmdir}/%{jrelnk_versionless_name}/bin
%define jrelnk_name		jre-%{version}.%{release}.%{_arch}
%define sdkbindir       %{_jvmdir}/%{sdkdir}/bin
%define jrebindir       %{_jvmdir}/%{jredir}/bin

%define jvmjardir       %{_jvmjardir}/%{uniquesuffix}

%define rpm_state_dir %{_localstatedir}/lib/rpm-state


Name:		%{purename}
Version:	%{version}
Release:	%{release}
Epoch:		1
Summary:	Super Java Runtime Environment
License:	Super License
Group:		Development/Interpreters

Provides:       jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{origin} = %{epoch}:%{version}-%{release}
Provides:       jre-%{javaver}, java-%{javaver}, jre = %{epoch}:%{javaver} 
Provides:	java-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java = %{epoch}:%{javaver}
Requires:	/usr/sbin/update-alternatives
Requires:	jpackage-utils >= 0:1.5.38

BuildRequires:	dos2unix, jpackage-utils >= 0:1.5.38, sed, %{_bindir}/perl
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils
Requires(post):   /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives
Requires(post):   perl
Requires(postun): perl
Requires:	copy-jdk-configs
BuildRequires:    desktop-file-utils

%description
This package contains the Super Java Runtime Environment.

%package devel
Summary:	Super Java Development Kit
Group:		Development/Compilers
Requires:	/usr/sbin/update-alternatives
Provides:       java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-sdk-%{origin} = %{epoch}:%{version}-%{release}
Provides:	java-sdk-%{javaver}, java-sdk = %{epoch}:%{javaver}
Provides:	java-devel-%{origin} = %{epoch}:%{version}-%{release}
Provides:       java-%{javaver}-devel, java-devel = %{epoch}:%{javaver}
Requires:	%{purename}%{_isa} = %{epoch}:%{version}-%{release}

%description devel
The Super Java Development Kit contains the software and tools that
developers need to compile, debug, and run applets and applications
written using the Java programming language.

%prep
prioritylength=`expr length %{priority}`
if [ $prioritylength -ne 6 ] ; then
 echo "priority must be 6 digits in total, violated"
 exit 14
fi

%build
rm -rf image
mkdir image
pushd image
mkdir -p jre/lib/security/
mkdir jre/bin
mkdir bin
mkdir -p conf/ecurity/policy
mkdir conf/management

echo "config1 %{uniquesuffix}" > jre/lib/security/cacerts
echo "config(noreplace)2 %{uniquesuffix}" > jre/lib/security/java.policy
echo "config(noreplace)3 %{uniquesuffix}" > jre/lib/security/java.security
echo "config4 %{uniquesuffix}" > jre/lib/security/blacklist

#marked == labeled in files as config/config(noreplace) 
mkdir -p conf/security/policy/unlimited/
mkdir -p conf/management/
#links are not marked, only targets are (should be default case?)
echo "config(noreplace), link to %{etcjavasubdir}/nvra/filrname %{uniquesuffix}" > "conf/security/policy/unlimited/default_US_export.policy"
echo "config(noreplace), link to %{etcjavasubdir}/nvra/filrname, constant" > "conf/security/java.policy"
echo "config, link to %{etcjavasubdir}/nvra/filrname %{uniquesuffix}" > "conf/security/java.security"
echo "config, link to %{etcjavasubdir}/nvra/filrname, constant" > "conf/logging.properties"
#both links and targets are marked
echo "config(noreplace), link to %{etcjavasubdir}/nvra/filrname %{uniquesuffix}" > "conf/security/nss.cfg"
echo "config(noreplace), link to %{etcjavasubdir}/nvra/filrname, constant" > "conf/management/jmxremote.access"
echo "config, link to %{etcjavasubdir}/nvra/filrname %{uniquesuffix}" > "conf/net.properties"
echo "config, link to %{etcjavasubdir}/nvra/filrname, constant" > "conf/sound.properties"
#only  links are marked,  targets are not (does it have sense?)
echo "config(noreplace), link to %{etcjavasubdir}/nvra/filrname %{uniquesuffix}" > "conf/management/jmxremote.password.template"
echo "config(noreplace), link to %{etcjavasubdir}/nvra/filrname, constant" > "conf/management/management.properties"
echo "config, link to %{etcjavasubdir}/nvra/filrname %{uniquesuffix}" > "conf/net2.properties"
echo "config, link to %{etcjavasubdir}/nvra/filrname, constant" > "conf/sound2.properties"


echo "%{uniquesuffix}" > jre/bin/java
echo "%{uniquesuffix}" > bin/java
echo "%{uniquesuffix}" > bin/javac
echo "%{uniquesuffix}" > jre/lib/some.lib.so
echo "%{uniquesuffix}" > jre/lib/security/local_policy.jar
popd

%install
rm -rf $RPM_BUILD_ROOT

# main files
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}

pushd $RPM_BUILD_ROOT%{_jvmdir}
ln -s %{jredir} %{jrelnk_name}
popd

mkdir $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib
mkdir $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/security
mkdir $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/lib/
mkdir $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/lib/security
mkdir $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/bin
mkdir $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/bin

cp image/jre/lib/security/cacerts $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/security/
cp image/jre/lib/security/java.policy $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/security/
cp image/jre/lib/security/java.security $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/security/
cp image/jre/lib/security/blacklist $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/security/

mv image/jre/lib/security/cacerts $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/lib/security/
mv image/jre/lib/security/java.policy $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/lib/security/
mv image/jre/lib/security/java.security $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/lib/security/
mv image/jre/lib/security/blacklist $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/lib/security/

mv  image/jre/bin/java $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/bin/java
mv  image/bin/java $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/bin/java
mv  image/bin/javac $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/bin/javac
mv  image/jre/lib/some.lib.so  $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib
mv  image/jre/lib/security/local_policy.jar $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/security


mkdir -p $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/conf/security/policy/unlimited/
mkdir -p $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/conf/management/
mkdir -p $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/jre/lib/

#links are not marked, only targets are (should be default case?)
mv "image/conf/security/policy/unlimited/default_US_export.policy" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/security/policy/unlimited/default_US_export.policy"
mv "image/conf/security/java.policy" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/security/java.policy"
mv "image/conf/security/java.security" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/security/java.security"
mv "image/conf/logging.properties" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/logging.properties"
#both links and targets are marked
mv "image/conf/security/nss.cfg" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/security/nss.cfg"
mv "image/conf/management/jmxremote.access" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/management/jmxremote.access"
mv "image/conf/net.properties" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/net.properties"
mv "image/conf/sound.properties" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/sound.properties"
#only  links are marked,  targets are not (does it have sense?)
mv "image/conf/management/jmxremote.password.template" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/management/jmxremote.password.template"
mv "image/conf/management/management.properties" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/management/management.properties"
mv "image/conf/net2.properties" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/net2.properties"
mv "image/conf/sound2.properties" $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/"conf/sound2.properties"


confEtcDir=%{etcjavadir}
confJvmDir=%{_jvmdir}/%{sdkdir}

mkdir -p $RPM_BUILD_ROOT/$confEtcDir
mkdir -p $RPM_BUILD_ROOT/$confEtcDir/lib


mv "$RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/lib/security/" $RPM_BUILD_ROOT/%{etcjavadir}/lib/
mv "$RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/conf" $RPM_BUILD_ROOT/%{etcjavadir}/

  # directories links
pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}
  ln -s $confEtcDir/conf  ./conf
popd
pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir}/lib/
  ln -s $confEtcDir/lib/security  ./security
popd


%clean
rm -rf $RPM_BUILD_ROOT

%post

# see pretrans where this file is declared
if [ -f %{_libexecdir}/copy_jdk_configs_fixFiles.sh ] ; then
  sh  %{_libexecdir}/copy_jdk_configs_fixFiles.sh %{rpm_state_dir}/%{name}.%{_arch}  %{_jvmdir}/%{sdkdir}
fi



%pretrans -p <lua>
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1290388 for pretrans over pre
-- if copy-jdk-configs is in transaction, it installs in pretrans to temp
-- if copy_jdk_configs is in temp, then it means that copy-jdk-configs is in tranasction  and so is
-- preferred over one in %%{_libexecdir}. If it is not in transaction, then depends 
-- whether copy-jdk-configs is installed or not. If so, then configs are copied
-- (copy_jdk_configs from %%{_libexecdir} used) or not copied at all
local posix = require "posix"
local debug = false

SOURCE1 = "%{rpm_state_dir}/copy_jdk_configs.lua"
SOURCE2 = "%{_libexecdir}/copy_jdk_configs.lua"

local stat1 = posix.stat(SOURCE1, "type");
local stat2 = posix.stat(SOURCE2, "type");

  if (stat1 ~= nil) then
  if (debug) then
    print(SOURCE1 .." exists - copy-jdk-configs in transaction, using this one.")
  end;
  package.path = package.path .. ";" .. SOURCE1
else 
  if (stat2 ~= nil) then
  if (debug) then
    print(SOURCE2 .." exists - copy-jdk-configs alrady installed and NOT in transation. Using.")
  end;
  package.path = package.path .. ";" .. SOURCE2
  else
    if (debug) then
      print(SOURCE1 .." does NOT exists")
      print(SOURCE2 .." does NOT exists")
      print("No config files will be copied")
    end
  return
  end
end
-- run contetn of included file with fake args
arg = {"--currentjvm", "%{uniquesuffix}", "--jvmdir", "%{_jvmdir}", "--origname", "%{name}", "--origjavaver", "%{javaver}", "--arch", "%{_arch}", "--temp", "%{rpm_state_dir}/%{name}.%{_arch}"}
require "copy_jdk_configs.lua"


%post devel
#update-alternatives --install %{_bindir}/javac javac %{sdk_versionless_bindir}/javac %{priority} \
#--slave %{_jvmdir}/java                     java_sdk                    %{_jvmdir}/%{sdkdir} 
#update-alternatives --install %{_jvmdir}/java-%{origin} java_sdk_%{origin} %{_jvmdir}/%{sdklnk_versionless_name} %{priority} \
#--slave %{_jvmjardir}/java-%{origin}        java_sdk_%{origin}_exports  %{_jvmjardir}/%{sdkdir}
#update-alternatives --install %{_jvmdir}/java-%{javaver_alternatives} java_sdk_%{javaver_alternatives} %{_jvmdir}/%{sdklnk_versionless_name} %{priority} \
#--slave %{_jvmjardir}/java-%{javaver_alternatives}       java_sdk_%{javaver_alternatives}_exports %{_jvmjardir}/%{sdkdir}

%postun
#update-alternatives --remove java %{jre_versionless_bindir}/java
#update-alternatives --remove \
# jce_%{javaver_alternatives}_%{origin}_local_policy.%{_arch} \
# %{_jvmprivdir}/%{uniquesuffix}/jce/vanilla/local_policy.jar
#update-alternatives --remove jre_%{origin}  %{_jvmdir}/%{jrelnk_versionless_name}
#update-alternatives --remove jre_%{javaver_alternatives} %{_jvmdir}/%{jrelnk_versionless_name}

%postun devel
#update-alternatives --remove javac %{sdk_versionless_bindir}/javac
#update-alternatives --remove java_sdk_%{origin}  %{_jvmdir}/%{sdklnk_versionless_name}
#update-alternatives --remove java_sdk_%{javaver_alternatives} %{_jvmdir}/%{sdklnk_versionless_name}



%files
%defattr(-,root,root)
%dir %{_jvmdir}/%{sdkdir}
%dir %{_jvmdir}/%{sdkdir}/lib
%dir %{_jvmdir}/%{jredir}
%dir %{_jvmdir}/%{jredir}/lib/security/
%dir %{_jvmdir}/%{jredir}/lib/
%{_jvmdir}/%{jrelnk_name}
%{jvmjardir}
%config %{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config %{_jvmdir}/%{jredir}/lib/security/blacklist
%ghost %{_jvmdir}/%{jredir}/lib/security/local_policy.jar
%{_jvmdir}/%{jredir}/lib/some.lib.so
%{_jvmdir}/%{jredir}/bin
# files are in etc, links are in jvmdir
%dir %{etcjavasubdir}
%dir %{etcjavadir}
%config(noreplace) %{etcjavadir}/conf/logging.properties
%config(noreplace) %{etcjavadir}/conf/management/jmxremote.access
%config(noreplace) %{etcjavadir}/conf/management/jmxremote.password.template
%config(noreplace) %{etcjavadir}/conf/management/management.properties
%config(noreplace) %{etcjavadir}/conf/net.properties
%config(noreplace) %{etcjavadir}/conf/net2.properties
%config(noreplace) %{etcjavadir}/conf/security/java.policy
%config(noreplace) %{etcjavadir}/conf/security/java.security
%config(noreplace) %{etcjavadir}/conf/security/nss.cfg
%config(noreplace) %{etcjavadir}/conf/security/policy/unlimited/default_US_export.policy
%config(noreplace) %{etcjavadir}/conf/sound.properties
%config(noreplace) %{etcjavadir}/conf/sound2.properties
%config(noreplace) %{etcjavadir}/lib/security/blacklist
%config(noreplace) %{etcjavadir}/lib/security/cacerts
%config(noreplace) %{etcjavadir}/lib/security/java.policy
%config(noreplace) %{etcjavadir}/lib/security/java.security
%{_jvmdir}/%{sdkdir}/conf
%{_jvmdir}/%{sdkdir}/lib/security


%files devel
%defattr(-,root,root)
%{_jvmdir}/%{sdkdir}/bin/*


%changelog
* Thu Dec 01 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.10.0.1-1
- nit

