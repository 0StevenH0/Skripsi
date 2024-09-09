import re
from collections import defaultdict


class KnowledgeHandler:
    __slots__ = ["text","level_patterns"]

    def __init__(self):
        self.text = None
        self.level_patterns = {
            "level_7": r"\[7\[(.*?)\]\]",
            "level_6": r"\[6\[(.*?)\]\]",
            "level_5": r"\[5\[(.*?)\]\]",
            "level_4": r"\[4\[(.*?)\]\]",
            "level_3": r"\[3\[(.*?)\]\]",
            "level_2": r"\[2\[(.*?)\]\]",
            "level_1": r"\[1\[(.*?)\]\]",
            "level_0": r"\[\[(.*?)\]\]"
        }

    def temporary_knowledge(self):

        text = {
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[AKUNTANSI]] [2[(@BEKASI)]] [[DESKRIPSI]]": "Accounting Technology Program, merupakan Program Sarjana Akuntansi, School of Accounting, Binus University yang berlokasi di Kampus Binus Bekasi. Program Sarjana Akuntansi ini menekankan pada kurikulum Akuntansi yang diintegrasikan pada penguasaan penerapan teknologi akuntansi (accounting software) bagi mahasiswanya",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[AKUNTANSI]] [2[(@BEKASI)]] [[PROSPEK KARIR]]": "Professional Accountant (yang fokus pada bidang, tetapi tidak terbatas sebagai) : Business Transformer, Data Navigator dan Digital Playmaker. Lulusan dapat juga berkarir sebagai Public Accountant, Management Accountant, Internal Auditor, Government Accountant, Government Auditor, Tax Consultant, Banker, Finance  Analyst, Entrepreneur",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[AKUNTANSI]] [2[(@BEKASI)]] [[AKREDITASI]]": " Unggul | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[AKUNTANSI]] [2[(@BEKASI)]] [[DURASI]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[AKUNTANSI]] [2[(@BEKASI)]] [[TITEL]]": "Ak.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[DESKRIPSI]]": "Fashion program BINUS UNIVERSITY telah berdiri sejak 2010 berawal dari hasil kolaborasi antara BINUS UNIVERSITY INTERNATIONAL dan Northumbria University, Newcastle, Inggris. Lalu per tahun ajaran 2024/2025 Fashion program hadir di BINUS @Alam Sutera dengan cita-cita dan semangat yang sama yaitu untuk menjadi sekolah Fashion terbaik di Indonesia, Fashion program terus mengupayakan menghasilkan tenaga profesional terampil yang mampu memecahkan masalah di bidang nya. Untuk mendukung kegiatan belajar mengajar yang efektif, BINUS UNIVERSITY menyediakan fasilitas studio yang sangat baik, termasuk ruang kerja produksi garmen, ruang eksperimen tekstil (batik, tenun, sablon dan rajut), laboratorium komputer, dan studio fotografi. Fashion Program menyediakan rencana studi personal yang fleksibel berdasarkan kebutuhan mahasiswa, didukung melalui program perkuliahan (2+1+1) dimana dalam 2,5 tahun kuliah mahasiswa di siapkan menggapai karier dan peluang Dual Degree (S.Ds. & BA with Hons.). Selain itu mahasiswa dapat memilih peminatan Fashion Design atau Fashion Retail Management, yang memberikan kesempatan untuk mendalami praktik fashion dan bekerja dalam industri fashion sesungguhnya. Fashion Program Binus University juga mengutamakan pengalaman praktis, proyek kolaboratif dengan profesional, dan mempersiapkan mahasiswa untuk mengembangkan keterampilan dan mempersiapkan karier mereka",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[PROSPEK KARIR]]": "Berbagai peluang karir di industri Fashion akan diperkenalkan dan mahasiswa akan dipersiapkan selama masa studi. Kurikulum terintegrasi dirancang dan dikembangkan untuk mendukung mahasiswa dalam membangun keterampilan teknis dan non-teknis serta terlibat dengan industry. Salah satu program dalam pengembangan karir yaitu program magang untuk setiap mahasiswa di mana mahasiswa dapat melakukan proyek nyata sebagai studi praktis dalam konteks industri. Program ini mengembangkan kemampuan siswa untuk terlibat dalam praktik profesional, dan tanggung jawab etika dan organisasi. Selain itu, serangkaian studi/kunjungan lapangan ke para profesional dan industri akan dilakukan untuk memberikan dasar yang baik untuk memiliki gambaran yang luas tentang industri. Pengalaman-pengalaman ini mendukung aspirasi karir individu dan dapat memberikan jaringan sosial dan profesional. Lulusan program Fashion diharapkan siap sebagai desainer untuk produksi dan manufaktur menengah hingga massal, sebagai tanggapan terhadap berbagai tingkat pasar. Lulusan Fashion program BINUS UNIVERSITY dapat berkarir dalam bidang berikut tanpa terkecuali ",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[AKREDITASI]]": "A | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[DURASI]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[TITEL]]": "S.Ds. & BA (Hons) (Optional)",
        }

        return text

    def make_level(self):
        text = self.temporary_knowledge()
        grouped_keys = defaultdict(list)

        for item in text.items():
            for level, pattern in self.level_patterns.items():
                matches = re.findall(pattern, item[0])
                if matches:
                    grouped_keys[level].extend(matches)
                else:
                    grouped_keys[level].append(None)
            grouped_keys["val"].append(item[1])

        return dict(grouped_keys)

    def make_condition(self,inputs):

        condition = ""
        for level, pattern in self.level_patterns.items():
            matches = re.findall(pattern, inputs)
            if matches:
                matches = [match.replace("'", "''") for match in matches]
                if len(matches) > 1:
                    cond = " OR ".join(f"'{match}'" for match in matches)
                    condition += f"AND ({level} IN ({cond})) "
                else:
                    cond = matches[0]
                    condition += f"AND {level} = '{cond}' "

        return condition


x = KnowledgeHandler()
print(x.make_level())
