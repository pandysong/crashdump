# crash dump tool

Often are log like blow is caputred in the linux console:

```
<4>[ 2240.408003] [<c0014088>] (unwind_backtrace+0x0/0xe0) from [<c00118cc>] (show_stack+0x10/0x14)
<4>[ 2240.408041] [<c00118cc>] (show_stack+0x10/0x14) from [<c00443ec>] (warn_slowpath_common+0x4c/0x68)
<4>[ 2240.408118] [<c0044420>] (warn_slowpath_null+0x18/0x1c) from [<c0703c50>] (clk_disable+0x18/0x24)
<4>[ 2240.408201] [<c06336b4>] (rk_camera_mclk_ctrl+0x300/0x39c) from [<c003f5a8>] (rk_sensor_ioctrl+0x1ec/0x26c)
<4>[ 2240.408281] [<c003f844>] (rk_sensor_pwrseq+0x1b4/0x230) from [<c003fae0>] (rk_sensor_power+0x220/0x2dc)
<4>[ 2240.408361] [<c0624108>] (soc_camera_power_off+0x20/0x70) from [<c0635b58>] (generic_sensor_s_power+0xd4/0xfc)
<4>[ 2240.408438] [<c06225bc>] (__soc_camera_power_off+0x3c/0x78) from [<c0623d64>] (soc_camera_close+0x74/0xb0)
<4>[ 2240.408518] [<c060b52c>] (v4l2_release+0x34/0x70) from [<c0120234>] (__fput+0xe8/0x1ec)
<4>[ 2240.408592] [<c0061478>] (task_work_run+0xbc/0xd4) from [<c0011178>] (do_work_pending+0x80/0x94)
```

It is quite tedious to analyse line by line.

The tool is used to convert numbers to file name and line number which could be
used to locate in the source code.

# How to use


```
python3 crashdump.py <log.txt> <elf_file>
```

<log.txt> is the file containing the logs shown above.
<elf_file> is the elf binary file, like `vmlinux`.


The output might be like:

```
kernel/arch/arm/kernel/unwind.c:409: [<c0014088>] (unwind_backtrace+0x0/0xe0) from [<c00118cc>] (show_stack+0x10/0x14)
kernel/arch/arm/kernel/traps.c:216: [<c00118cc>] (show_stack+0x10/0x14) from [<c00443ec>] (warn_slowpath_common+0x4c/0x68)
kernel/kernel/panic.c:455: [<c0044420>] (warn_slowpath_null+0x18/0x1c) from [<c0703c50>] (clk_disable+0x18/0x24)
kernel/drivers/media/video/rk30_camera_oneframe.c:1390: [<c06336b4>] (rk_camera_mclk_ctrl+0x300/0x39c) from [<c003f5a8>] (rk_sensor_ioctrl+0x1ec/0x26c)
kernel/arch/arm/mach-rockchip/rk_camera.c:1178 (discriminator 3): [<c003f844>] (rk_sensor_pwrseq+0x1b4/0x230) from [<c003fae0>] (rk_sensor_power+0x220/0x2dc)
kernel/drivers/media/platform/soc_camera/soc_camera.c:92: [<c0624108>] (soc_camera_power_off+0x20/0x70) from [<c0635b58>] (generic_sensor_s_power+0xd4/0xfc)
kernel/drivers/media/platform/soc_camera/soc_camera.c:122: [<c06225bc>] (__soc_camera_power_off+0x3c/0x78) from [<c0623d64>] (soc_camera_close+0x74/0xb0)
kernel/drivers/media/v4l2-core/v4l2-dev.c:162: [<c060b52c>] (v4l2_release+0x34/0x70) from [<c0120234>] (__fput+0xe8/0x1ec)
kernel/kernel/task_work.c:82 (discriminator 1): [<c0061478>] (task_work_run+0xbc/0xd4) from [<c0011178>] (do_work_pending+0x80/0x94)
```

# Use in vim: cfile

You may save above output to a file, and then in Vim, you could load and parse the file, using 

```
:cfile <the_out_put_file>
```

