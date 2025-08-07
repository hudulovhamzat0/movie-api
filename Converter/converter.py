import pandas as pd
import json
import gzip
import numpy as np
from typing import Optional

def clean_nan_values(obj):
    """
    NaN, inf ve diğer problematik değerleri temizle
    """
    if isinstance(obj, dict):
        return {k: clean_nan_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan_values(item) for item in obj]
    elif pd.isna(obj) or obj is np.nan:
        return None
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return float(obj)
    elif isinstance(obj, str) and obj.lower() in ['nan', 'null', '\\n', '']:
        return None
    else:
        return obj

def convert_imdb_tsv_to_json(tsv_file_path: str, output_json_path: str, max_rows: Optional[int] = None):
    """
    IMDb TSV dosyasını JSON formatına dönüştürür (NaN değerleri düzeltilmiş)
    """
    try:
        print(f"Dosya okunuyor: {tsv_file_path}")
        
        # TSV dosyasını oku
        df = pd.read_csv(tsv_file_path, 
                        sep='\t', 
                        compression='gzip',
                        na_values=['\\N', 'NaN', 'nan', 'NULL', 'null', ''],
                        keep_default_na=True,
                        nrows=max_rows,
                        low_memory=False,
                        dtype=str)  # Önce her şeyi string olarak oku
        
        print(f"Toplam {len(df)} kayıt okundu")
        print("Sütunlar:", list(df.columns))
        
        # Veri temizliği ve tip dönüştürme
        print("Veri temizliği yapılıyor...")
        
        # Sayısal sütunları belirle ve dönüştür
        numeric_columns = []
        
        # title.basics için numeric columns
        title_numeric = ['isAdult', 'startYear', 'endYear', 'runtimeMinutes']
        # name.basics için numeric columns  
        name_numeric = ['birthYear', 'deathYear']
        
        # Hangi sütunlar mevcut, onu kontrol et
        for col in title_numeric + name_numeric:
            if col in df.columns:
                numeric_columns.append(col)
        
        # Sayısal sütunları dönüştür
        for col in numeric_columns:
            print(f"Sayısal sütun dönüştürülüyor: {col}")
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # NaN değerleri None'a dönüştür
            df[col] = df[col].replace({np.nan: None})
        
        # Tüm string sütunlardaki NaN değerleri None'a dönüştür
        string_columns = [col for col in df.columns if col not in numeric_columns]
        for col in string_columns:
            df[col] = df[col].replace({np.nan: None, 'nan': None, 'NaN': None, '\\N': None})
        
        # DataFrame'i dictionary'lere dönüştür
        print("JSON'a dönüştürülüyor...")
        json_data = []
        
        for _, row in df.iterrows():
            # Her satırı dictionary'e dönüştür
            record = {}
            for col in df.columns:
                value = row[col]
                
                # NaN kontrolü
                if pd.isna(value) or value is np.nan:
                    record[col] = None
                elif isinstance(value, str) and value.lower() in ['nan', 'null', '\\n']:
                    record[col] = None
                elif isinstance(value, (np.int64, np.int32)):
                    record[col] = int(value) if not pd.isna(value) else None
                elif isinstance(value, (np.float64, np.float32)):
                    if pd.isna(value) or np.isnan(value) or np.isinf(value):
                        record[col] = None
                    else:
                        record[col] = float(value)
                else:
                    record[col] = value
            
            json_data.append(record)
        
        # Final temizlik
        json_data = clean_nan_values(json_data)
        
        # JSON dosyasına yaz
        print("JSON dosyası yazılıyor...")
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, 
                     indent=2, 
                     ensure_ascii=False, 
                     separators=(',', ': '),
                     default=lambda x: None if pd.isna(x) else str(x))
        
        print(f"✅ Başarıyla dönüştürüldü: {output_json_path}")
        print(f"📊 JSON dosyası {len(json_data)} kayıt içeriyor")
        
        # JSON validation test
        print("🔍 JSON validation testi...")
        try:
            with open(output_json_path, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
            print("✅ JSON dosyası geçerli!")
        except json.JSONDecodeError as e:
            print(f"❌ JSON validation hatası: {e}")
        
        return json_data
        
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()
        return None

def preview_data(tsv_file_path: str, num_rows: int = 5):
    """
    TSV dosyasının ilk birkaç satırını önizle
    """
    try:
        df = pd.read_csv(tsv_file_path, 
                        sep='\t', 
                        compression='gzip',
                        na_values=['\\N', 'NaN', 'nan', 'NULL', 'null'],
                        nrows=num_rows,
                        dtype=str)
        
        print("📋 Veri önizlemesi:")
        print("="*60)
        print(df.head())
        print(f"\n📊 Sütun bilgileri:")
        print(df.info())
        print(f"\n📝 Sütun isimleri: {list(df.columns)}")
        
        # NaN değerlerini kontrol et
        print(f"\n🔍 NaN değer kontrolü:")
        for col in df.columns:
            nan_count = df[col].isna().sum()
            if nan_count > 0:
                print(f"  - {col}: {nan_count} NaN değer")
        
        return df
        
    except Exception as e:
        print(f"❌ Önizleme hatası: {e}")
        return None

def convert_large_tsv_streaming(tsv_file_path: str, output_json_path: str, chunk_size: int = 10000):
    """
    Büyük dosyalar için streaming converter (NaN değerleri düzeltilmiş)
    """
    try:
        print(f"🚀 Streaming conversion başlıyor...")
        
        with open(output_json_path, 'w', encoding='utf-8') as f:
            f.write('[\n')
            
            first_record = True
            total_rows = 0
            
            # Chunk'lar halinde işle
            chunk_reader = pd.read_csv(tsv_file_path, 
                                     sep='\t', 
                                     compression='gzip',
                                     na_values=['\\N', 'NaN', 'nan', 'NULL', 'null', ''],
                                     keep_default_na=True,
                                     chunksize=chunk_size,
                                     low_memory=False,
                                     dtype=str)
            
            for chunk_num, chunk in enumerate(chunk_reader, 1):
                print(f"📦 Chunk {chunk_num} işleniyor... ({len(chunk)} kayıt)")
                
                # Sayısal sütunları dönüştür
                numeric_columns = []
                for col in ['isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'birthYear', 'deathYear']:
                    if col in chunk.columns:
                        numeric_columns.append(col)
                        chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
                
                # Her satırı işle
                for _, row in chunk.iterrows():
                    record = {}
                    for col in chunk.columns:
                        value = row[col]
                        
                        if pd.isna(value):
                            record[col] = None
                        elif col in numeric_columns:
                            if pd.isna(value):
                                record[col] = None
                            else:
                                record[col] = int(value) if value == int(value) else float(value)
                        else:
                            record[col] = str(value) if value is not None else None
                    
                    # JSON'a yaz
                    if not first_record:
                        f.write(',\n  ')
                    else:
                        f.write('  ')
                        first_record = False
                    
                    json.dump(record, f, ensure_ascii=False, default=str)
                    total_rows += 1
                
                print(f"  ✅ Toplam işlenen: {total_rows} kayıt")
            
            f.write('\n]')
            
        print(f"🎉 Streaming conversion tamamlandı!")
        print(f"📊 Toplam {total_rows} kayıt işlendi")
        
        # Validation test
        print("🔍 JSON validation testi...")
        try:
            with open(output_json_path, 'r', encoding='utf-8') as f:
                json.load(f)
            print("✅ JSON dosyası geçerli!")
        except json.JSONDecodeError as e:
            print(f"❌ JSON validation hatası: {e}")
        
    except Exception as e:
        print(f"❌ Streaming conversion hatası: {e}")
        import traceback
        traceback.print_exc()

# Ana program
if __name__ == "__main__":
    print("🎬 IMDb TSV to JSON Converter (NaN Fixed)")
    print("="*50)
    
    # Dosya yolları
    tsv_file = "/home/hudul/Masaüstü/Projects/movie-api/1. Convert/title.basics.tsv.gz"
    json_file = "data.json"
    
    # Önizleme
    print("👀 Veri önizlemesi yapılıyor...")
    preview_data(tsv_file, 3)
    
    print("\n" + "="*50 + "\n")
    
    # Dönüştürme seçeneği
    print("Dönüştürme seçenekleri:")
    print("1. Normal conversion (hızlı, daha fazla RAM)")
    print("2. Streaming conversion (yavaş, az RAM)")
    
    choice = input("Seçiminiz (1 veya 2): ").strip()
    
    if choice == "2":
        print("🌊 Streaming conversion seçildi...")
        convert_large_tsv_streaming(tsv_file, json_file, chunk_size=5000)
    else:
        print("⚡ Normal conversion seçildi...")
        result = convert_imdb_tsv_to_json(
            tsv_file_path=tsv_file,
            output_json_path=json_file,
            max_rows=10000  # Test için sınırlı
        )
        
        if result:
            print("\n📄 İlk kaydın JSON formatı:")
            print("-" * 40)
            print(json.dumps(result[0], indent=2, ensure_ascii=False))
    
    print("\n🎉 İşlem tamamlandı!")