#! /bin/env ruby

require 'getoptlong'
require 'Dir'


#############################################################
infile = nil
outdir = nil

gff_lines = Hash.new{|h,k|h[k]=[]}


#############################################################
opts = GetoptLong.new(
  ["-i", GetoptLong::REQUIRED_ARGUMENT],
  ["--outdir", GetoptLong::REQUIRED_ARGUMENT],
)

opts.each do |opt, value|
  case opt
    when '-i'
      infile = value
    when '--outdir'
      outdir = value
  end
end

if infile.nil?
  raise "infile has to be given! Exiting ......"
end
if outdir.nil?
  raise "outdir has to be given! Exiting ......"
end

mkdir_with_force(outdir, true)


#############################################################
File.open(infile, 'r').each_line do |line|
  line.chomp!
  line_arr = line.split("\t")
  attr = line_arr[-1]
  gene=$1 if attr =~ /=([^;=]+)/
  gff_lines[gene] << line
end


gff_lines.each_pair do |gene, list|
  outfile = File.join([outdir, gene])
  out_fh = File.open(outfile, 'w')
  out_fh.puts list
  out_fh.close
end


