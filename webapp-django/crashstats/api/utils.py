import humanfriendly

from crashstats.base.templatetags.jinja_helpers import is_dangerous_cpu
from crashstats.base.utils import urlencode_obj
from crashstats.crashstats.templatetags.jinja_helpers import (
    booleanish_to_boolean,
    human_readable_iso_date,
    timestamp_to_date
)


def transform_report_details(report, raw_crash, crashing_thread, parsed_dump, descriptions):
    report_data = {
        'uuid': report.get('uuid'),
        'signature': report.get('signature'),
        'dateProcessed': human_readable_iso_date(report.get('date_processed')),
        'uptime': get_duration_data(report.get('uptime')),
        'lastCrash': get_duration_data(report.get('last_crash')),
        'installAge': get_duration_data(report.get('install_age')),
        'product': report.get('product'),
        'releaseChannel': report.get('release_channel'),
        'version': report.get('version'),
        'build': report.get('build'),
        'os': report.get('os_pretty_version') or report.get('os_name'),
        'osVersion': report.get('os_version'),
        'cpuName': report.get('cpu_name'),
        'cpuInfo': report.get('cpu_info'),
        'isDangerousCpu': is_dangerous_cpu(report.get('cpu_name'), report.get('cpu_info')),
        'processType': report.get('process_type'),
        'pluginName': report.get('PluginName'),
        'pluginVersion': report.get('PluginVersion'),
        'pluginFilename': report.get('PluginFilename'),
        'crashReason': report.get('reason'),
        'crashAddress': report.get('address'),
        'addonsChecked': report.get('addons_checked'),
        'appNotes': report.get('app_notes'),
        'processorNotes': report.get('processor_notes'),
    }
    raw_crash_data = {
        'installTime': timestamp_to_date(raw_crash.get('InstallTime')),
        'androidVersion': raw_crash.get('Android_Version'),
        'b2gOsVersion': raw_crash.get('B2G_OS_Version'),
        'androidManufacturer': raw_crash.get('Android_Manufacturer'),
        'androidModel': raw_crash.get('Android_Model'),
        'androidCpuAbi': raw_crash.get('Android_CPU_ABI'),
        'adapterVendorId': raw_crash.get('AdapterVendorID'),
        'adapterDeviceId': raw_crash.get('AdapterDeviceID'),
        'statupCrash': raw_crash.get('StatupCrash'),
        'isStartupCrash': booleanish_to_boolean(raw_crash.get('StartupCrash')),
        'remoteType': raw_crash.get('RemoteType'),
        'flashProcessDump': raw_crash.get('FlashProcessDump'),
        'mozCrashReason': raw_crash.get('MozCrashReason'),
        'totalVirtualMemory': get_filesize_data(raw_crash.get('TotalVirtualMemory')),
        'availableVirtualMemory': get_filesize_data(raw_crash.get('AvailableVirtualMemory')),
        'availablePageFile': get_filesize_data(raw_crash.get('AvailablePageFile')),
        'availablePhysicalMemory': get_filesize_data(raw_crash.get('AvailablePhysicalMemory')),
        'oomAllocationSize': get_filesize_data(raw_crash.get('OOMAllocationSize')),
        'javaStackTrace': raw_crash.get('JavaStackTrace'),
        'systemMemoryUsePercentage': raw_crash.get('SystemMemoryUsePercentage'),
        'accessibility': raw_crash.get('Accessibility'),
    }
    memeory_measures_data = {}
    if 'memory_measures' in report:
        memeory_measures_data = {
            'memory_measures': get_filesize_data(report.memory_measures.explicit),
            'gfx_textures': get_filesize_data(report.memory_measures.gfx_textures),
            'ghost_windows': get_filesize_data(report.memory_measures.ghost_windows),
            'heap_allocated': get_filesize_data(report.memory_measures.heap_allocated),
            'heap_overhead': get_filesize_data(report.memory_measures.heap_overhead),
            'heap_unclassified': get_filesize_data(report.memory_measures.heap_unclassified),
            'host_object_urls': get_filesize_data(report.memory_measures.host_object_urls),
            'images': get_filesize_data(report.memory_measures.images),
            'js_main_runtime': get_filesize_data(report.memory_measures.js_main_runtime),
            'private': get_filesize_data(report.memory_measures.private),
            'resident': get_filesize_data(report.memory_measures.resident),
            'resident_unique': get_filesize_data(report.memory_measures.resident_unique),
            'system_heap_allocated':
                get_filesize_data(report.memory_measures.system_heap_allocated),
            'top_none_detached': get_filesize_data(report.memory_measures.top_none_detached),
            'vsize': get_filesize_data(report.memory_measures.vsize),
            'vsize_max_contiguous': get_filesize_data(report.memory_measures.vsize_max_contiguous),
        }
    threads_data = []
    if crashing_thread is not None:
        threads_data = [
            {
                'thread': thread.get('thread'),
                'name': thread.get('thread_name'),
                'frames': [
                    {
                        'frame': frame.get('frame'),
                        'isMissingSymbols': frame.get('missing_symbols'),
                        'module': frame.get('module'),
                        'signature': frame.get('signature'),
                        'sourceLink': frame.get('source_link'),
                        'file': frame.get('file'),
                        'line': frame.get('line'),
                    }
                    for frame in thread.get('frames')
                ]
            }
            for thread in parsed_dump.get('threads')
        ]
    descriptions_data = {
        'report': {
            'signature': descriptions.get('processed_crash.signature'),
            'uuid': descriptions.get('processed_crash.uuid'),
            'dateProcessed': descriptions.get('processed_crash.date_processed'),
            'uptime': descriptions.get('processed_crash.uptime'),
            'lastCrash': descriptions.get('processed_crash.last_crash'),
            'installAge': descriptions.get('processed_crash.install_age'),
            'product': descriptions.get('processed_crash.product'),
            'releaseChannel': descriptions.get('processed_crash.release_channel'),
            'version': descriptions.get('processed_crash.version'),
            'build': descriptions.get('processed_crash.build'),
            'os': descriptions.get('processed_crash.os_pretty_version'),
            'osVersion': descriptions.get('processed_crash.os_version'),
            'cpuName': descriptions.get('processed_crash.cpu_name'),
            'cpuInfo': descriptions.get('processed_crash.cpu_info'),
            'processType': descriptions.get('processed_crash.process_type'),
            'crashReason': descriptions.get('processed_crash.reason'),
            'crashAddress': descriptions.get('processed_crash.address'),
            'addonsChecked': descriptions.get('processed_crash.addons_checked'),
            'appNotes': descriptions.get('processed_crash.app_notes'),
            'processorNotes': descriptions.get('processed_crash.processor_notes'),
        },
        'rawCrash': {
            'installTime': descriptions.get('raw_crash.InstallTime'),
            'androidVersion': descriptions.get('raw_crash.Android_Version'),
            'b2gOsVersion': descriptions.get('raw_crash.B2G_OS_Version'),
            'androidManufacturer': descriptions.get('raw_crash.Android_Manufacturer'),
            'androidModel': descriptions.get('raw_crash.Android_Model'),
            'androidCpuAbi': descriptions.get('raw_crash.Android_CPU_ABI'),
            'adapterVendorId': descriptions.get('raw_crash.AdapterVendorID'),
            'adapterDeviceId': descriptions.get('raw_crash.AdapterDeviceID'),
            'isStartupCrash': descriptions.get('raw_crash.StartupCrash'),
            'flashProcessDump': descriptions.get('raw_crash.FlashProcessDump'),
            'mozCrashReason': descriptions.get('raw_crash.MozCrashReason'),
            'javaStackTrace': descriptions.get('processed_crash.java_stack_trace'),
            'totalVirtualMemory': descriptions.get('raw_crash.TotalVirtualMemory'),
            'availableVirtualMemory': descriptions.get('raw_crash.AvailableVirtualMemory'),
            'availablePageFile': descriptions.get('raw_crash.AvailablePageFile'),
            'availablePhysicalMemory': descriptions.get('raw_crash.AvailablePhysicalMemory'),
            'systemMemoryUsePercentage': descriptions.get('raw_crash.SystemMemoryUsePercentage'),
            'oomAllocationSize': descriptions.get('raw_crash.OOMAllocationSize'),
            'accessibility': descriptions.get('raw_crash.Accessibility'),
        },
    }

    query_string = urlencode_obj({'q': report.get('signature')})
    return {
        'report': report_data,
        'rawCrash': raw_crash_data,
        'memoryMeasures': memeory_measures_data,
        'crashingThread': crashing_thread,
        'threads': threads_data,
        'descriptions': descriptions_data,
        'sumoLink': 'https://support.mozilla.org/search?{}'.format(query_string),
        'mdnLink': 'https://developer.mozilla.org/en-US/docs/Understanding_crash_reports',
    }


def get_filesize_data(bytes):
    if bytes is None:
            return {}
    return {
        'formatted': format(int(bytes), ','),
        'bytes': bytes,
        'humanfriendly': humanfriendly.format_size(int(bytes))
    }


def get_duration_data(seconds):
    if seconds is None:
        return {}
    return {
        'formatted': format(int(seconds), ','),
        'seconds': seconds,
        'humanfriendly': humanfriendly.format_timespan(int(seconds)),
    }