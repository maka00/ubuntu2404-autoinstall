# Ubuntu 24.04 setup

The goal is to create a Ubuntu 24.04 image with a predefined user, network-setup, harddisk preparation and some basic packages installed without having to have a user interaction during the installation process.

# Required tools
```
7z 
xorriso
wget
task (https://taskfile.dev/)
```
# autoinstall.yaml
prepare the [autoinstall.yaml.jinja](tool/autoinstall.yaml.jinja) file.
Add software packages as you like.

create a .env file along the autoinstall.yaml.jinja file with the content:
```
DEVICEHOSTNAME=<servername>
USERNAME=<user>
PASSWORD=<password>
KEYBOARDLAYOUT=<keyboardlayout>
TIMEZONE=<timezone>
SSH_KEY_PUB=<text file containing sshpubkey (one per line)>
```

If `SSH_KEY_PUB` is not set the sshd will allow password authentication. 
If it is set you have to prepare a secrets.txt file with all public keys which shall have remote access to the machine.

The `PASSWORD` content has to be generated with:
```bash
openssl passwd
```

Generate the actual autoinstall.yaml file with:
`task generate-autoinstall`.
This wil generate an autoinstall.yaml file in the root folder.

# prepare ISO images

1) Perform a `task download` to download the Ubuntu server image to the (iso)[iso/] folder.

2) Extract the ISO image with `task extract-iso`.
in (extracted/boot/grub/grub.cfg)[extracted/boot/grub/grub.cfg] change the entry

```
	linux	/casper/vmlinuz ---
``` 

to

```
	linux	/casper/vmlinuz autoinstall ---
```

This is necessary or the installation process will ask for a confirmation during the process.

3) Get the iso information:

`task print-torito` 

```
xorriso : NOTE : Loading ISO image tree from LBA 0
xorriso : UPDATE :    1065 nodes read in 1 seconds
libisofs: NOTE : Found hidden El-Torito image for EFI.
libisofs: NOTE : EFI image start and size: 1351729 * 2048 , 10144 * 512
xorriso : NOTE : Detected El-Torito boot information which currently is set to be discarded
Drive current: -indev 'iso/ubuntu-24.04.1-live-server-amd64.iso'
Media current: stdio file, overwriteable
Media status : is written , is appendable
Boot record  : El Torito , MBR protective-msdos-label grub2-mbr cyl-align-off GPT
Media summary: 1 session, 1354431 data blocks, 2645m data, 4093g free
Volume id    : 'Ubuntu-Server 24.04.1 LTS amd64'
-V 'Ubuntu-Server 24.04.1 LTS amd64'
--modification-date='2024082715393700'
--grub2-mbr --interval:local_fs:0s-15s:zero_mbrpt,zero_gpt:'iso/ubuntu-24.04.1-live-server-amd64.iso'
--protective-msdos-label
-partition_cyl_align off
-partition_offset 16
--mbr-force-bootable
-append_partition 2 28732ac11ff8d211ba4b00a0c93ec93b --interval:local_fs:5406916d-5417059d::'iso/ubuntu-24.04.1-live-server-amd64.iso'
-appended_part_as_gpt
-iso_mbr_part_type a2a0d0ebe5b9334487c068b6b72699c7
-c '/boot.catalog'
-b '/boot/grub/i386-pc/eltorito.img'
-no-emul-boot
-boot-load-size 4
-boot-info-table
--grub2-boot-info
-eltorito-alt-boot
-e '--interval:appended_partition_2_start_1351729s_size_10144d:all::'
-no-emul-boot
-boot-load-size 10144
```

and create from that information a shell script:
| change | from | to |
|--------|------|----|
| add line | | `-o autoinstall-ubuntu-24.04.1-live-server-amd64.iso` |
| change line | `--grub2-mbr --interval:local_fs:0s-15s:zero_mbrpt,zero_gpt:'iso/ubuntu-24.04.1-live-server-amd64.iso'` | `--grub2-mbr BOOT/1-Boot-NoEmul.img`
| change line | `-append_partition 2 28732ac11ff8d211ba4b00a0c93ec93b --interval:local_fs:5406916d-5417059d::'iso/ubuntu-24.04.1-live-server-amd64.iso'` | `-append_partition 2 28732ac11ff8d211ba4b00a0c93ec93b BOOT/2-Boot-NoEmul.img`
| add line | | `extracted`

Be sure that each line except the last ends with an \ (no space after the backslash!)

Here is the corresponding output:
```bash
#!/bin/env bash

xorriso -as mkisofs -r \
-V 'Ubuntu-Server 24.04.1 LTS amd64' \
-o autoinstall-ubuntu-24.04.1-live-server-amd64.iso \
--modification-date='2024082715393700' \
--grub2-mbr BOOT/1-Boot-NoEmul.img \
--protective-msdos-label \
-partition_cyl_align off \
-partition_offset 16 \
--mbr-force-bootable \
-append_partition 2 28732ac11ff8d211ba4b00a0c93ec93b BOOT/2-Boot-NoEmul.img \
-appended_part_as_gpt \
-iso_mbr_part_type a2a0d0ebe5b9334487c068b6b72699c7 \
-c '/boot.catalog' \
-b '/boot/grub/i386-pc/eltorito.img' \
-no-emul-boot \
-boot-load-size 4 \
-boot-info-table \
--grub2-boot-info \
-eltorito-alt-boot \
-e '--interval:appended_partition_2_start_1351729s_size_10144d:all::' \
-no-emul-boot \
-boot-load-size 10144 \
extracted
```

# create the ISO image

Run `task build-iso` to build the `autoinstall-ubuntu-24.04.1-live-server-amd64.iso`




