"""
@author: zachary.vinyard@oneacrefund.org
example script for business innovations associate interview
"""
import os, sys
import pandas as pd
import math
from datetime import datetime

#version number
version = '2-15-6'

#FILEPATH - CHANGE THIS TO THE FILE DIRECTORY FOR YOUR COMPUTER
filepath = os.path.expanduser('~' ) + r'\Documents\Tubura\data'

#FILENAME - CHANGE TO MATCH THE INPUT FILE NAME
filename = 'pnseb-input.xlsx'

#sheet names
reps_sheet = 'REPS'
groups_sheet = 'GROUPS'

#voucher sizes
max_fert_vouchers = 12
fert_voucher_size = 25
max_lime_vouchers = 15
lime_voucher_size = 50

#prioritization algorithm - choose prioritize, no_prioritization
prioritization_algorithm = 'prioritize'

#DEBUG
debug = False

def main():
	time = datetime.now()
	datestring_for_file = '%04d%02d%02d%02d%02d%02d' % (time.year, time.month, time.day, time.hour,time.minute, time.second)
	outfile_name ='pnseb_matching_out_%s_%s.xlsx' % (version, datestring_for_file)
	debug_outfile_name = 'pnseb_matching_out_debug_%s_%s.xlsx' % (version, datestring_for_file)
	prog_announcement('starting - %04d-%02d-%02d %02d:%02d:%02d\nversion - %s' % (time.year, time.month, time.day, time.hour,time.minute, time.second, version))
	prog_announcement('loading data - %s' % filename)
	os.chdir(filepath)
	try:
		xl_file = pd.ExcelFile(filename)
		reps = xl_file.parse(sheet_name = reps_sheet)
		groups = xl_file.parse(sheet_name = groups_sheet)
		del xl_file
	except TypeError:
		xl_file = pd.ExcelFile(filename)
		reps = xl_file.parse(sheet_name = reps_sheet)
		groups = xl_file.parse(sheet_name = groups_sheet)
		del xl_file
	except FileNotFoundError:
		prog_announcement('file not found - program terminated')
		return None
	except KeyboardInterrupt:
		prog_announcement('keyboard interrupt - program terminated')
		return None
	prog_announcement('cleaning columns')
	try:
		reps, groups = col_clean(reps), col_clean(groups)
	except KeyboardInterrupt:
		prog_announcement('keyboard interrupt - program terminated')
		return None
	except:
		prog_announcement('columns improperly formated - program terminated')
		return None
	try:
		assigned, unassigned, m_groups, no_reps = allocate_vouchers(groups, reps)
		if debug:
			prog_announcement('writing to file - %s' % debug_outfile_name)
			assigned_df = pd.DataFrame(assigned, columns = ['oaf_unique_id', 'name', 'assigned_group', 'group_id', 'match_type', 'ucid', 'group', 'lime_vouchers', 'dap_vouchers', 'npk_vouchers', 'uree_vouchers', 'government_province', 'government_commune', 'government_colline'])
			assigned_df.set_index('oaf_unique_id', inplace = True)
			#assigned_df.sort_index(axis = 0, inplace = True)
			unassigned_df = pd.DataFrame(unassigned, columns = ['oaf_unique_id', 'name', 'assigned_group', 'group_id', 'match_type', 'ucid', 'group', 'lime_vouchers', 'dap_vouchers', 'npk_vouchers', 'uree_vouchers', 'government_province', 'government_commune', 'government_colline'])
			unassigned_df.set_index('oaf_unique_id', inplace = True)
			#unassigned_df.sort_index(axis = 0, inplace = True)
			groups_df = pd.DataFrame(groups, columns = ['group_id', 'group_name', 'ucid', 'lime_demand', 'lime_remaining', 'dap_demand', 'dap_remaining', 'npk_demand', 'npk_remaining', 'uree_demand', 'uree_remaining', 'government_province', 'government_commune', 'government_colline'])
			groups_df.set_index('group_id', inplace = True)
			groups_df.sort_index(axis = 0, inplace = True)
			no_reps_df = pd.DataFrame(no_reps)
			xl_writer_debug = pd.ExcelWriter(debug_outfile_name)
			assigned_df.to_excel(xl_writer_debug,sheet_name = 'assigned_to_group')
			unassigned_df.to_excel(xl_writer_debug, sheet_name = 'unassigned')
			groups_df.to_excel(xl_writer_debug, sheet_name = 'groups')
			no_reps_df.to_excel(xl_writer_debug, sheet_name = 'no_reps')
			try:
				xl_writer_debug.save()
				del xl_writer_debug
			except PermissionError:
				prog_announcement('file is open, cannot save debug file')
		s_assigned, s_unassigned, s_groups, s_no_reps = allocate_vouchers(pd.DataFrame(m_groups), pd.DataFrame(unassigned), match_type = 'site', priority = algorithms[prioritization_algorithm])
	except GroupsEmptyError:
		prog_announcement('data contains no groups - programe terminated')
		return None
	except KeyboardInterrupt:
		prog_announcement('keyboard interrupt - program terminated')
		return None
	except DataFormatError:
		prog_announcement('critical error - program terminated')
		return None
	except:
		prog_announcement('unexpected error - program terminated')
		return None
	prog_announcement('writing to file - %s' % outfile_name)
	assigned_df = pd.DataFrame(s_assigned + assigned, columns = ['oaf_unique_id', 'name', 'assigned_group', 'group_id', 'match_type', 'ucid', 'group', 'lime_vouchers', 'dap_vouchers', 'npk_vouchers', 'uree_vouchers', 'government_province', 'government_commune', 'government_colline']) if len(s_assigned) > 0 else pd.DataFrame(assigned, columns = ['oaf_unique_id', 'name', 'assigned_group', 'group_id', 'match_type', 'ucid', 'group', 'lime_vouchers', 'dap_vouchers', 'npk_vouchers', 'uree_vouchers', 'government_province', 'government_commune', 'government_colline'])
	assigned_df.set_index('oaf_unique_id', inplace = True)
	assigned_df.sort_index(axis = 0, inplace = True)
	unassigned_df = pd.DataFrame(s_unassigned, columns = ['oaf_unique_id', 'name', 'assigned_group', 'group_id', 'match_type', 'ucid', 'group', 'lime_vouchers', 'dap_vouchers', 'npk_vouchers', 'uree_vouchers', 'government_province', 'government_commune', 'government_colline'])
	unassigned_df.set_index('oaf_unique_id', inplace = True)
	unassigned_df.sort_index(axis = 0, inplace = True)
	groups_df = pd.DataFrame(s_groups, columns = ['group_id', 'priority', 'group_name', 'ucid', 'lime_demand', 'lime_remaining', 'dap_demand', 'dap_remaining', 'npk_demand', 'npk_remaining', 'uree_demand', 'uree_remaining', 'government_province', 'government_commune', 'government_colline'])
	if not debug:
		groups_df.drop('priority', axis = 1, inplace = True)
	groups_df.set_index('group_id', inplace = True)
	groups_df.sort_index(axis = 0, inplace = True)
	#no_reps_df = pd.DataFrame(no_reps)
	file_information = {'version' : version, 'input_file' : filename, 'outfile_name' : outfile_name, 'debug' : debug, 'elapsed_time' : datetime.now() - time}
	if debug:
		file_information['input_reps'] = len(reps)
	file_information['output_reps'] = len(assigned_df) + len(unassigned_df)
	if debug:
		file_information['input_groups'] = len(groups)
	file_information['output_groups'] = len(groups_df)
	file_information_df = pd.DataFrame.from_dict(data = file_information, orient = 'index')
	file_information_df.columns = ['information']
	xl_writer = pd.ExcelWriter(outfile_name)
	assigned_df.to_excel(xl_writer,sheet_name = 'assigned_to_group')
	unassigned_df.to_excel(xl_writer, sheet_name = 'unassigned')
	groups_df.to_excel(xl_writer, sheet_name = 'groups')
	file_information_df.to_excel(xl_writer, sheet_name = 'file_information')
	#no_reps_df.to_excel(xl_writer, sheet_name = 'no_reps')
	try:
		xl_writer.save()
		del xl_writer
	except PermissionError:
		prog_announcement('file is open, cannot save - program terminated')
		return None
	except KeyboardInterrupt:
		prog_announcement('keyboard interrupt - program terminated')
		return None
	time2 = datetime.now()
	elapsed = time2 - time
	prog_announcement('elapsed time : %s\ncomplete - %04d-%02d-%02d %02d:%02d:%02d\n' % (elapsed, time2.year, time2.month, time2.day, time2.hour, time2.minute, time2.second))

def col_clean(dataframe):
	cols = dataframe.columns
	cols = cols.map(lambda x: x.strip().replace(' ', '_').lower() if isinstance(x, (str, 'unicode')) else x)
	dataframe.columns = cols
	dataframe['ucid'] = dataframe.apply(lambda row : '-'.join([row.government_province.strip().lower(),row.government_commune.strip().lower(),row.government_colline.strip().lower()]), axis = 1)
	return dataframe
	
def prog_bar(loc, length, barlen = 20):
	sys.stdout.flush()
	percent = int(((loc + 1) / length)*100)
	prog = int(((loc + 1)/ length)*barlen)
	sys.stdout.write('\r')
	sys.stdout.write('[%s%s] - %s %%' % ('='*prog, ' '*(barlen - prog), percent))
	if(percent == 100):
		sys.stdout.write('\n')
	
def prog_announcement(text):
	sys.stdout.flush()
	sys.stdout.write('\r')
	sys.stdout.write(text)
	sys.stdout.write('\n')
	
def allocate_vouchers(groups, reps, match_type = 'group', priority = None):
	if not( match_type == 'group' or match_type == 'site'):
		raise ValueError('match_type must be \'group\' or \'site\'')
	elif len(groups) == 0:
		raise GroupsEmptyError('data includes no groups')
	elif match_type != 'group' and priority == None:
		raise DataFormatError('no matching algorithm included')
	elif len(groups['group_id']) != len(groups['group_id'].unique()):
		raise DataFormatError('group ids not unique')
	prog_announcement('starting matching on %s' % match_type)
	unassigned = []
	assigned = []
	no_reps = []
	groups_updated = []
	assigned_client_ids = []
	unassigned_client_ids = []
	sites = groups['ucid'].unique()
	alg = priority
	if match_type == 'site':
		try:
			reps_backup = reps.set_index('oaf_unique_id')
			unassigned_client_ids = list(set(reps['oaf_unique_id']))
		except KeyError:
			if len(reps) == 0:
				prog_announcement('no reps available for site - level matching')
				return (reps, reps, groups, unassigned_client_ids)
			else:
				raise KeyError
		groups = alg(groups)
	groups, reps = groups.set_index('ucid'), reps.set_index('ucid')
	for site in sites:
		prog_bar(list(sites).index(site), len(sites))
		no_site_reps = False
		g = groups.loc[site]
		try:
			if match_type == 'group':
				r = reps
			elif match_type == 'site':
				r = reps.loc[site]
		except KeyError:
			no_reps.append(site)
			no_site_reps = True
		if match_type == 'group':
			gids = pd.Series(g['group_id']).unique()
		elif match_type == 'site':
			gids = pd.Series(g['priority'])
		for gid in gids:
			try:
				if match_type == 'group':
					g_row = g.loc[g['group_id'] == gid]
					npk_voucher_count = int(g_row.loc[site, 'npk_demand']) / fert_voucher_size
					uree_voucher_count = int(g_row.loc[site, 'uree_demand']) / fert_voucher_size
					dap_voucher_count = int(g_row.loc[site, 'dap_demand']) / fert_voucher_size
					lime_voucher_count = int(g_row.loc[site, 'lime_demand']) / lime_voucher_size
				elif match_type == 'site':
					g_row = g.loc[g['priority'] == gid]
					npk_voucher_count = int(g_row.loc[site, 'npk_remaining']) / fert_voucher_size
					uree_voucher_count = int(g_row.loc[site, 'uree_remaining']) / fert_voucher_size
					dap_voucher_count = int(g_row.loc[site, 'dap_remaining']) / fert_voucher_size
					lime_voucher_count = int(g_row.loc[site, 'lime_remaining']) / lime_voucher_size
			except KeyError:
				g_row = g
				if match_type == 'group':
					npk_voucher_count = int(g_row['npk_demand']) / fert_voucher_size
					uree_voucher_count = int(g_row['uree_demand']) / fert_voucher_size
					dap_voucher_count = int(g_row['dap_demand']) / fert_voucher_size
					lime_voucher_count = int(g_row['lime_demand']) / lime_voucher_size
				elif match_type == 'site':
					npk_voucher_count = int(g_row['npk_remaining']) / fert_voucher_size
					uree_voucher_count = int(g_row['uree_remaining']) / fert_voucher_size
					dap_voucher_count = int(g_row['dap_remaining']) / fert_voucher_size
					lime_voucher_count = int(g_row['lime_remaining']) / lime_voucher_size
			if not no_site_reps:
				try:
					if match_type == 'group':
						clients = r.loc[r['group_id'] == gid]['oaf_unique_id']
					elif match_type == 'site':
						clients = pd.Series(r['oaf_unique_id'])
				except KeyError:
					clients = pd.Series(r['oaf_unique_id'])
				for client in clients:
					if match_type == 'site' and client in assigned_client_ids:
						if client in unassigned_client_ids:
							unassigned_client_ids.remove(client)
						continue
					client_npk, client_dap, client_uree, client_lime = 0, 0, 0, 0
					client_voucher_count = 0
					if npk_voucher_count > 0:
						npk_available_to_add = min(npk_voucher_count, max_fert_vouchers - client_voucher_count)
						client_npk += npk_available_to_add
						client_voucher_count += npk_available_to_add
						npk_voucher_count = npk_voucher_count - npk_available_to_add
					if client_voucher_count < max_fert_vouchers and dap_voucher_count > 0:
						dap_available_to_add = min(dap_voucher_count, max_fert_vouchers - client_voucher_count)
						client_dap += dap_available_to_add
						client_voucher_count += dap_available_to_add
						dap_voucher_count = dap_voucher_count - dap_available_to_add
					if client_voucher_count < max_fert_vouchers and uree_voucher_count > 0:
						uree_available_to_add = min(uree_voucher_count, max_fert_vouchers - client_voucher_count)
						client_uree += uree_available_to_add
						client_voucher_count += uree_available_to_add
						uree_voucher_count = uree_voucher_count - uree_available_to_add
					if lime_voucher_count > 0:
						client_lime += min(lime_voucher_count, max_lime_vouchers - client_lime)
						lime_voucher_count -= client_lime
					client_dict = {}
					if match_type == 'group':
						client_row = r.loc[r['oaf_unique_id'] == client]
						for label in client_row.columns:
							client_dict[label] = client_row.iloc[0][label]
					elif match_type == 'site':
						try:
							client_row = r.loc[r['oaf_unique_id'] == client]
							for label in client_row.columns:
								client_dict[label] = client_row.loc[site, label]
						except KeyError:
							for label, val in r.iteritems():
								client_dict[label] = val
					client_dict['npk_vouchers'], client_dict['dap_vouchers'], client_dict['uree_vouchers'], client_dict['lime_vouchers'] = math.ceil(client_npk), math.ceil(client_dap), math.ceil(client_uree), math.ceil(client_lime)
					client_dict['match_type'] = match_type
					if match_type == 'group':
						client_dict['assigned_group'] = gid
					if match_type == 'site':
						try:
							client_dict['assigned_group'] = g_row.loc[site, 'group_id']
						except KeyError:
							client_dict['assigned_group'] = g_row['group_id']
						except:
							raise DataFormatError('error')
					client_dict['ucid'] = site
					if (client_voucher_count <= 0 and client_lime <= 0):
						if match_type == 'group':
							unassigned.append(client_dict)
					else:
						assigned.append(client_dict)
						assigned_client_ids.append(client)
						if match_type == 'site':
							if client in unassigned_client_ids:
								unassigned_client_ids.remove(client)
			group_dict = {}
			group_dict['ucid'] = site
			try:
				for label in g_row.columns:
					group_dict[label] = g_row.loc[site, label]
			except (AttributeError, KeyError) as e:
				for label, val in g_row.iteritems():
					group_dict[label] = val
			group_dict['npk_remaining'] = int(npk_voucher_count) * fert_voucher_size
			group_dict['dap_remaining'] = int(dap_voucher_count) * fert_voucher_size
			group_dict['uree_remaining'] = int(uree_voucher_count) * fert_voucher_size
			group_dict['lime_remaining'] = int(lime_voucher_count) * lime_voucher_size
			groups_updated.append(group_dict)
		if match_type == 'site':
			groups = alg(groups, re = True)
	#prog_announcement('finalizing client lists for %s matching' % match_type)
	try:
		clients_not_in_group = reps.loc[~reps['group_id'].isin(groups['group_id'])]['oaf_unique_id']
	except ValueError:
		clients_not_in_group = pd.Series(r['oaf_unique_id'])
	if len(clients_not_in_group) >0:
		prog_announcement('finalizing client lists for %s matching' % match_type)
	for client in clients_not_in_group:
		prog_bar(list(clients_not_in_group).index(client), len(clients_not_in_group))
		client_npk, client_dap, client_uree, client_lime = 0, 0, 0, 0
		client_dict = {}
		try:
			client_row = reps.loc[reps['oaf_unique_id'] == client]
			for label in client_row.columns:
				client_dict[label] = client_row.iloc[0][label]
		except KeyError:
			raise DataFormatError
		client_dict['npk_vouchers'], client_dict['dap_vouchers'], client_dict['uree_vouchers'], client_dict['lime_vouchers'] = client_npk, client_dap, client_uree, client_lime
		client_dict['match_type'] = match_type
		client_dict['assigned_group'] = client_dict['group_id']
		client_dict['ucid'] = '-'.join([client_dict['government_province'].strip().lower(),client_dict['government_commune'].strip().lower(),client_dict['government_colline'].strip().lower()])
		unassigned.append(client_dict)
	if match_type == 'site':
		unassigned = reps_backup.loc[list(set(unassigned_client_ids))].reset_index().to_dict()
	prog_announcement('completed matching on %s' % match_type)
	return (assigned, unassigned, groups_updated, unassigned_client_ids)

class DataFormatError (Exception):
	pass

class GroupsEmptyError (Exception):
	pass

def prioritize(groups, re = False):
	if re or 'priority' in groups.columns:
		groups.drop('priority', axis = 1, inplace = True)
	groups['total_fert'] = groups.apply(lambda row : row.dap_remaining + row.npk_remaining + row.uree_remaining, axis = 1)
	groups.sort_values(by = 'total_fert', ascending = False, axis = 0, inplace = True)
	groups['priority'] = [x for x in range(1, len(groups) + 1)]
	groups.drop('total_fert', axis = 1, inplace = True)
	return groups

def no_prioritization(groups, re = False):
	if re:
		groups.drop('priority', axis = 1, inplace = 1)
	groups['priority'] = groups.apply(lambda row : row.group_id, axis = 1)
	return groups

algorithms = {'prioritize' : prioritize, 'no_prioritization' : no_prioritization}

if __name__ ==  '__main__':
	main()
